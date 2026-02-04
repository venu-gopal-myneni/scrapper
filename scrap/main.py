from extract import download_files
from validate import validate_files, DROP_EMPTY_STR_ROWS, SCHEMA_DICT
from datetime import date
import os


date_today = date.today() # date(year=2026, month=1, day=23) 
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
    validate_files(extract_keys_dict,SCHEMA_DICT, DROP_EMPTY_STR_ROWS, date_folder, BUCKET)

if __name__ == "__main__":
    main()