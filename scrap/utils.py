import os
import boto3
from dotenv import load_dotenv
import duckdb


load_dotenv()

BUCKET = os.getenv("S3_BUCKET")
AWS_PROFILE = os.getenv("AWS_PROFILE")

S3_CLIENT = boto3.client("s3")


def get_extensions():
    out = set()
    con = duckdb.connect()

    exts = con.execute("""
    SELECT extension_name
    FROM duckdb_extensions()
    WHERE installed = true
    """).fetchall()

    for (ext,) in exts:
        out.add(ext)
    return out


def get_ducklake_conn():
    con = duckdb.connect()

    con.execute("LOAD ducklake")

    con.execute(f"""
    CREATE OR REPLACE SECRET secret (TYPE s3,PROVIDER credential_chain,CHAIN config,PROFILE '{AWS_PROFILE}');
                """)

    # catalog_path = f"s3://{BUCKET}/ducklake/catalog.ducklake"
    catalog_path = "catalog.ducklake"
    data_path = f"s3://{BUCKET}/ducklake/data/"

    con.execute(f"""
    ATTACH 'ducklake:{catalog_path}'
    AS lake
    (DATA_PATH '{data_path}');
    """)

    con.execute("USE lake")
    return con
