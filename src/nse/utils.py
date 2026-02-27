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


def create_tables(con):
    # con.execute("DROP TABLE IF EXISTS pd;")
    out = con.execute("""
        CREATE TABLE IF NOT EXISTS pd (
    date DATE,
    market VARCHAR(2),
    series VARCHAR(4),
    symbol VARCHAR(20),
    security VARCHAR(20),
    prev_close_price FLOAT,
    open_price FLOAT,
    high_price FLOAT,
    low_prrice FLOAT,
    close_price FLOAT,
    net_trade_val FLOAT,
    net_trade_qty FLOAT,
    ind_sec VARCHAR(1),
    corp_ind VARCHAR(4),
    num_trades FLOAT,
    high_52_wk FLOAT,
    low_52_wk FLOAT,
    source_file VARCHAR(250),
    created_at TIMESTAMP 
);
""")

    print(out.fetchall())

    # con.execute("DROP TABLE IF EXISTS sec;")

    out = con.execute(""" 
CREATE TABLE IF NOT EXISTS sec
 (
    symbol VARCHAR(20),
    series VARCHAR(4),
    date DATE,
    prev_close_price FLOAT,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    last_price FLOAT,
    close_price FLOAT,
    avg_price FLOAT,
    net_trade_qty FLOAT,
    turnover_lacs FLOAT,
    num_trades FLOAT,
    deliver_qty FLOAT,
    deliver_per FLOAT,
    source_file VARCHAR(250),
    created_at TIMESTAMP 
    
);
""")

    print(out.fetchall())

if __name__ == "__main__":
    create_tables(get_ducklake_conn())
