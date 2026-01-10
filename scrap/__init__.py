import zipfile

import requests
import boto3
from io import BytesIO
from datetime import date
from pathlib import Path

date_today = date.today()
formatted_date_today = date_today.strftime("%d%m%y")

URLS = {
    f"PR{formatted_date_today}.zip": f"https://nsearchives.nseindia.com/archives/equities/bhavcopy/pr/PR{formatted_date_today}.zip"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
    "Connection": "keep-alive",
}
BUCKET = None

s3 = boto3.client("s3")


def download_as_is(urls: list[str], date_today: str):
    for filename, url in urls.items():
        key = f"{date_today}/{filename}"
        buffer = BytesIO()

        with requests.get(url, headers=headers, stream=True, timeout=30) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                buffer.write(chunk)

        buffer.seek(0)

        s3.upload_fileobj(
            buffer, BUCKET, key, ExtraArgs={"ContentType": "application/zip"}
        )


def download_extracted(urls: list[str], date_today: str):
    for filename, url in urls.items():
        base_name = Path(filename).stem
        buffer = BytesIO()

        with requests.get(url, headers=headers, stream=True, timeout=30) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                buffer.write(chunk)

        buffer.seek(0)

        with zipfile.ZipFile(buffer) as z:
            for name in z.namelist():
                with z.open(name) as f:
                    s3.upload_fileobj(
                        f, BUCKET, f"{date_today}/{base_name}/unzipped/{name}"
                    )

if __name__ == "__main__":

    download_extracted(URLS, formatted_date_today)
    download_as_is(URLS, formatted_date_today)