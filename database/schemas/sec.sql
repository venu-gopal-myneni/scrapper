CREATE TABLE sec
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


MERGE INTO sec AS t
USING (
    SELECT
        *,
    filename AS source_file,
    CURRENT_TIMESTAMP AS created_at
        
    FROM read_parquet('sec.parquet')
) AS s
ON (t.symbol = s.symbol AND t.series = s.series)

WHEN MATCHED THEN UPDATE 
WHEN NOT MATCHED THEN INSERT ;