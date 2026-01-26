import polars as pl
from pathlib import Path

DROP_EMPTY_STR_ROWS = {"pd": ["mkt"]}
SCHEMA_DICT = {
    "sec_bhavdata_full": {
        "sec_bhavdata_full": {
            "SYMBOL": "symbol",
            " SERIES": "series",
            " DATE1": "date",
            " PREV_CLOSE": "prev_close",
            " OPEN_PRICE": "open_price",
            " HIGH_PRICE": "high_price",
            " LOW_PRICE": "low_price",
            " LAST_PRICE": "last_price",
            " CLOSE_PRICE": "close_price",
            " AVG_PRICE": "avg_price",
            " TTL_TRD_QNTY": "ttl_trd_qnty",
            " TURNOVER_LACS": "turnover_lacs",
            " NO_OF_TRADES": "no_of_trades",
            " DELIV_QTY": "deliv_qty",
            " DELIV_PER": "deliv_per",
        }
    },
    "PR": {
        "pd": {
            "MKT": "mkt",
            "SERIES": "series",
            "SYMBOL": "symbol",
            "SECURITY": "security",
            "PREV_CL_PR": "prev_close",
            "OPEN_PRICE": "open_price",
            "HIGH_PRICE": "high_price",
            "LOW_PRICE": "low_prrice",
            "CLOSE_PRICE": "close_price",
            "NET_TRDVAL": "net_tdval",
            "NET_TRDQTY": "net_trdqty",
            "IND_SEC": "ind_sec",
            "CORP_IND": "corp_ind",
            "TRADES": "trades",
            "HI_52_WK": "hi_42_wk",
            "LO_52_WK": "lo_52-wk",
        }
    },
}


def validate_files(keys_dicts, schema_dict, drop_empty_str_rows, date_folder, bucket):
    # read
    for folder, list in keys_dicts.items():
        for file in list:
            basename = Path(file).stem
            if basename in schema_dict[folder]:
                schema = schema_dict[folder][basename]
                read_key = f"s3://{bucket}/{file}"
                df = pl.read_csv(read_key)
                df = df.rename(schema)
                empty_str_rows = drop_empty_str_rows.get(basename, None)
                if empty_str_rows:
                    df = df.filter(~pl.any_horizontal(pl.col(empty_str_rows).eq("")))
                key = f"validate/{date_folder}/{basename}.parquet"
                s3_loc = f"s3://{bucket}/{key}"
                df.write_parquet(s3_loc)
                print(f"Validated file written to {key} in bucket {bucket}")
