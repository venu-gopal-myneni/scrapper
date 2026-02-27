import polars as pl
from pathlib import Path

from pandera.polars import Column, DataFrameSchema, Check


def transform_sec(df: pl.DataFrame) -> pl.DataFrame:
    df = df.with_columns(pl.col(pl.String).str.strip_chars())
    df = df.with_columns(pl.col("date").str.strptime(pl.Date, "%d-%b-%Y"))
    for col in ["deliver_qty", "deliver_per"]:
        df = df.with_columns(pl.col(col).cast(pl.Float64, strict=False))
    return df


def transform_pd(df: pl.DataFrame) -> pl.DataFrame:
    df = df.with_columns(pl.col(pl.String).str.strip_chars())
    return (
        df
        # drop invalid MKT rows
        .filter(pl.col("market").str.contains(r"^[A-Za-z]$"))
        # conditional replacements
        .with_columns(
            [
                pl.when(pl.col("market") == "Y")
                .then(pl.lit("market"))
                .otherwise(pl.col("series"))
                .alias("series"),
                pl.when(pl.col("market") == "Y")
                .then(pl.col("security"))
                .otherwise(pl.col("symbol"))
                .alias("symbol"),
            ]
        )
    )


PD_SCHEMA_CHECK = DataFrameSchema(
    {
        "market": Column(pl.Utf8, Check.str_matches(r"^[A-Za-z]$")),
        "series": Column(pl.Utf8),
        "symbol": Column(pl.Utf8),
        "security": Column(pl.Utf8),
        "prev_close_price": Column(pl.Float64, nullable=True),
        "open_price": Column(pl.Float64, nullable=True),
        "high_price": Column(pl.Float64, nullable=True),
        "low_price": Column(pl.Float64, nullable=True),
        "close_price": Column(pl.Float64, nullable=True),
        "net_trade_val": Column(pl.Float64, nullable=True),
        "net_trade_qty": Column(pl.Int64, nullable=True),
        "ind_sec": Column(pl.Utf8, nullable=True),
        "corp_ind": Column(pl.Utf8, nullable=True),
        "num_trades": Column(pl.Int64, nullable=True),
        "high_52_wk": Column(pl.Float64, nullable=True),
        "low_52_wk": Column(pl.Float64, nullable=True),
    },
    # 🔴 uniqueness constraint
    # checks=[
    #     Check(
    #         lambda df: ~df.filter(pl.struct(["symbol", "series"]).is_duplicated()).any(),
    #         error="(symbol, series) combination must be unique",
    #     )
    # ],
    coerce=True,
)


SEC_SCHEMA_CHECK = DataFrameSchema(
    {
        "series": Column(pl.Utf8),
        "symbol": Column(pl.Utf8),
        "date": Column(pl.Date),
        "prev_close_price": Column(pl.Float64, nullable=True),
        "open_price": Column(pl.Float64, nullable=True),
        "high_price": Column(pl.Float64, nullable=True),
        "low_price": Column(pl.Float64, nullable=True),
        "last_price": Column(pl.Float64, nullable=True),
        "close_price": Column(pl.Float64, nullable=True),
        "avg_price": Column(pl.Float64, nullable=True),
        "net_trade_qty": Column(pl.Int64, nullable=True),
        "turnover_lacs": Column(pl.Float64, nullable=True),
        "num_trades": Column(pl.Int64, nullable=True),
        "deliver_qty": Column(pl.Float64, nullable=True),
        "deliver_per": Column(pl.Float64, nullable=True),
    },
    # 🔴 uniqueness constraint
    # checks=[
    #     Check(
    #         lambda df: ~df.filter(pl.struct(["symbol", "series"]).is_duplicated()).any(),
    #         error="(symbol, series) combination must be unique",
    #     )
    # ],
    coerce=True,
)


FOLDER_FILE_TRANSFORMS = {
    "sec_bhavdata_full": {
        "sec_bhavdata_full": {
            "COLUMN_RENAME": {
                "SYMBOL": "symbol",
                " SERIES": "series",
                " DATE1": "date",
                " PREV_CLOSE": "prev_close_price",
                " OPEN_PRICE": "open_price",
                " HIGH_PRICE": "high_price",
                " LOW_PRICE": "low_price",
                " LAST_PRICE": "last_price",
                " CLOSE_PRICE": "close_price",
                " AVG_PRICE": "avg_price",
                " TTL_TRD_QNTY": "net_trade_qty",
                " TURNOVER_LACS": "turnover_lacs",
                " NO_OF_TRADES": "num_trades",
                " DELIV_QTY": "deliver_qty",
                " DELIV_PER": "deliver_per",
            },
            "TRANSFORM_FUNCTION": transform_sec,
            "PANDERA_CHECK": SEC_SCHEMA_CHECK,
        }
    },
    "PR": {
        "pd": {
            "COLUMN_RENAME": {
                "MKT": "market",
                "SERIES": "series",
                "SYMBOL": "symbol",
                "SECURITY": "security",
                "PREV_CL_PR": "prev_close_price",
                "OPEN_PRICE": "open_price",
                "HIGH_PRICE": "high_price",
                "LOW_PRICE": "low_price",
                "CLOSE_PRICE": "close_price",
                "NET_TRDVAL": "net_trade_val",
                "NET_TRDQTY": "net_trade_qty",
                "IND_SEC": "ind_sec",
                "CORP_IND": "corp_ind",
                "TRADES": "num_trades",
                "HI_52_WK": "high_52_wk",
                "LO_52_WK": "low_52_wk",
            },
            "TRANSFORM_FUNCTION": transform_pd,
            "PANDERA_CHECK": PD_SCHEMA_CHECK,
        }
    },
}


def validate_files(keys_dicts, schema_dict, date_folder, bucket, local=True):
    """
    Docstring for validate_files

    :param keys_dicts:
            {
            'PR': ['raw/20-02-2026/PR/an.txt', 'raw/20-02-2026/PR/bc.csv', 'raw/20-02-2026/PR/bh.csv',
            'raw/20-02-2026/PR/bm.txt', 'raw/20-02-2026/PR/corpbond.csv', 'raw/20-02-2026/PR/etf.csv',
            'raw/20-02-2026/PR/gl.csv', 'raw/20-02-2026/PR/hl.csv', 'raw/20-02-2026/PR/mcap.csv',
            'raw/20-02-2026/PR/pd.csv', 'raw/20-02-2026/PR/pr.csv', 'raw/20-02-2026/PR/readme.txt',
            'raw/20-02-2026/PR/sme.csv', 'raw/20-02-2026/PR/tt.csv'],
            'sec_bhavdata_full': ['raw/20-02-2026/sec_bhavdata_full.csv']
            }
    :param schema_dict: Description
    :param date_folder: Description
    :param bucket: Description
    """
    # read
    for folder, list in keys_dicts.items():
        for file in list:
            basename = Path(file).stem
            if basename in schema_dict[folder]:
                # Read
                read_key = f"s3://{bucket}/{file}"
                df = pl.read_csv(read_key)

                rename_map = schema_dict[folder][basename]["COLUMN_RENAME"]
                tranform_func = schema_dict[folder][basename]["TRANSFORM_FUNCTION"]
                pandera_check = schema_dict[folder][basename]["PANDERA_CHECK"]

                # Validate
                df = df.rename(rename_map)
                df = tranform_func(df)
                df = pandera_check.validate(df)

                # Write
                key = f"validate/{date_folder}/{basename}.parquet"
                s3_loc = f"s3://{bucket}/{key}"
                if local:
                    df.write_parquet(f"{basename}.parquet")
                else:
                    df.write_parquet(s3_loc)

                print(f"Validated file written to {key} in bucket {bucket}")
