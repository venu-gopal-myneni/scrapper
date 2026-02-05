import zipfile

import requests
from io import BytesIO
from collections import defaultdict

from utils import S3_CLIENT

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
    "Connection": "keep-alive",
}


def download_files(urls: list[str], date_today: str, bucket: str) -> dict:
    keys_dict = defaultdict(list)
    for folder, url in urls.items():
        print(f"Downloading {folder} for date {date_today}")
        buffer = BytesIO()

        with requests.get(url, headers=HEADERS, stream=True, timeout=30) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                buffer.write(chunk)

        buffer.seek(0)

        content_type = get_content_type(r)
        print(f"content type is {content_type}")

        if content_type == "zip":
            with zipfile.ZipFile(buffer) as z:
                for name in z.namelist():
                    with z.open(name) as f:
                        name = name.translate(str.maketrans("", "", "0123456789"))
                        key = f"raw/{date_today}/{folder}/{name}"
                        print(f"Uploading file {key} to bucket {bucket}")
                        S3_CLIENT.upload_fileobj(f, bucket, key)
                        keys_dict[folder].append(key)
        elif content_type == "csv":
            key = f"raw/{date_today}/{folder}.csv"
            print(f"Uploading file {key} to bucket {bucket}")
            S3_CLIENT.upload_fileobj(buffer, bucket, key)
            keys_dict[folder].append(key)
    return keys_dict


def get_content_type(resp):
    content_type = resp.headers.get("Content-Type", "").lower()
    if content_type == "application/zip":
        return "zip"
    elif content_type == "text/csv":
        return "csv"
    else:
        raise ValueError(f"Unknown content type : {content_type}")
