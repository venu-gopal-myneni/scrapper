from extract import download_files
from validate import validate_files, FOLDER_FILE_TRANSFORMS

from ingest import merge_into_pd_table, merge_into_sec_table
from datetime import date
import os


date_today = date(
    year=2026, month=2, day=20
)  # date.today()  # date(year=2026, month=1, day=23)
date_folder = date_today.strftime("%d-%m-%Y")
formatted_date_today_ddmmyy = date_today.strftime("%d%m%y")
formatted_date_today_ddmmyyyy = date_today.strftime("%d%m%Y")
BUCKET = os.getenv("S3_BUCKET")


# https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_21012026.csv
# https://nsearchives.nseindia.com/archives/equities/bhavcopy/pr/PR210126.zip

URLS = {
    "PR": f"https://nsearchives.nseindia.com/archives/equities/bhavcopy/pr/PR{formatted_date_today_ddmmyy}.zip",
    "sec_bhavdata_full": f"https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{formatted_date_today_ddmmyyyy}.csv",
}


def main():
    extract_keys_dict = download_files(URLS, date_folder, BUCKET)
    print(f"Extract Keys Dict : \n {extract_keys_dict}")
    validate_files(extract_keys_dict, FOLDER_FILE_TRANSFORMS, date_folder, BUCKET, False)
    merge_into_pd_table(BUCKET, date_folder)
    merge_into_sec_table(BUCKET, date_folder)


if __name__ == "__main__":
    main()
