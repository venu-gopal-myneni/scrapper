CREATE TABLE pd (
    date DATE,
    market VARCHAR(2),
    series VARCHAR(4),
    symbol VARCHAR(20),
    security VARCHAR(20),
    prev_close FLOAT,
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

MERGE INTO silver.pd AS t
USING (
    SELECT 
        *,
        filename AS source_file,
        strptime(
    regexp_extract(filename, '/([0-9]{2}-[0-9]{2}-[0-9]{4})/', 1),
    '%Y/%m/%d'
  ) AS 'date'
    FROM read_parquet('s3://my-bucket/incoming/customers/*.parquet')
) AS s
ON (t.date = s.date AND t.market = s.market)

WHEN MATCHED THEN UPDATE 
WHEN NOT MATCHED THEN INSERT ;
