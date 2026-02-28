from nse.extract import download_files
from nse.validate import validate_files, FOLDER_FILE_TRANSFORMS

from nse.ingest import merge_into_pd_table, merge_into_sec_table
from datetime import date, datetime
import os
import argparse
from argparse import Namespace


BUCKET = os.getenv("S3_BUCKET")


# https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_21012026.csv
# https://nsearchives.nseindia.com/archives/equities/bhavcopy/pr/PR210126.zip


def get_args() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        type=str,
        help="Any day where NSE is not on holiday.Example: '15-01-2026'",
    )

    args = parser.parse_args()
    return args


def main():
    args = get_args()
    date_folder = args.date
    if not date_folder:
        date_today = date.today()
        date_folder = date_today.strftime("%d-%m-%Y")
        formatted_date_today_ddmmyy = date_today.strftime("%d%m%y")
        formatted_date_today_ddmmyyyy = date_today.strftime("%d%m%Y")

    else:
        date_today_input = datetime.strptime(date_folder, "%d-%m-%Y")
        formatted_date_today_ddmmyy = date_today_input.strftime("%d%m%y")
        formatted_date_today_ddmmyyyy = date_today_input.strftime("%d%m%Y")
    URLS = {
        "PR": f"https://nsearchives.nseindia.com/archives/equities/bhavcopy/pr/PR{formatted_date_today_ddmmyy}.zip",
        "sec_bhavdata_full": f"https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{formatted_date_today_ddmmyyyy}.csv",
    }

    extract_keys_dict = download_files(URLS, date_folder, BUCKET)
    print(f"Extract Keys Dict : \n {extract_keys_dict}")
    validate_files(
        extract_keys_dict, FOLDER_FILE_TRANSFORMS, date_folder, BUCKET, False
    )
    merge_into_pd_table(BUCKET, date_folder)
    merge_into_sec_table(BUCKET, date_folder)
