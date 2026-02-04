import os
import boto3
from dotenv import load_dotenv

load_dotenv()

BUCKET = os.getenv("S3_BUCKET")
S3_REGION=os.getenv("S3_REGION")
S3_ACCESS_KEY_ID=os.getenv("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY=os.getenv("S3_SECRET_ACCESS_KEY")

s3_client = boto3.client("s3")

import duckdb

con = duckdb.connect()

# Install DuckLake extension
con.execute("INSTALL ducklake;")
print("Installed ducklake")
con.execute("LOAD ducklake;")

# Set AWS credentials (or use IAM role if on EC2)
con.execute(f"""
SET s3_region={S3_REGION};
SET s3_access_key_id={S3_ACCESS_KEY_ID};
SET s3_secret_access_key={S3_SECRET_ACCESS_KEY};
""")
print("Set secrets")


con.execute(f"""
ATTACH 'ducklake:s3://{BUCKET}/ducklake/catalog.duckdb'
AS lake
(DATA_PATH 's3://{BUCKET}/ducklake/data/');
""")
print("Attached ducklake")


con.execute("USE lake")
con.execute("""
CREATE TABLE events (
    id INTEGER,
    event_name TEXT,
    event_time TIMESTAMP
);
""")
print("Created table")


