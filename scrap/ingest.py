from utils import get_ducklake_conn

def merge_into(bucket, date_today):
    con = get_ducklake_conn()
    sql_st = f"""
    
                MERGE INTO pd AS t
                USING (
                    SELECT
                    strptime(
                    regexp_extract(filename, '/([0-9]{2}-[0-9]{2}-[0-9]{4})/', 1),
                    '%d-%m-%Y'
                ) AS 'date',
                        *,
                    filename AS source_file,
                    CURRENT_TIMESTAMP AS created_at
                        
                    FROM read_parquet('s3://{bucket}/validate/{date_today}/pd.parquet')
                ) AS s
                ON (t.date = s.date AND t.market = s.market)

                WHEN MATCHED THEN UPDATE 
                WHEN NOT MATCHED THEN INSERT ;
"""
    out = con.execute(sql_st)