from nse.utils import get_ducklake_conn


def merge_into_pd_table(bucket, date_today):
    con = get_ducklake_conn()
    sql_st = f"""
    
                MERGE INTO pd AS t
                USING (
                    SELECT
                    strptime(
                    regexp_extract(filename, '/([0-9]{{2}}-[0-9]{{2}}-[0-9]{{4}})/', 1),
                    '%d-%m-%Y'
                ) AS date,
                        *,
                    filename AS source_file,
                    CURRENT_TIMESTAMP AS created_at
                        
                    FROM read_parquet('s3://{bucket}/validate/{date_today}/pd.parquet')
                ) AS s
                ON (t.symbol = s.symbol AND t.series = s.series AND t.date = s.date)

                WHEN MATCHED THEN UPDATE 
                WHEN NOT MATCHED THEN INSERT ;
"""
    print(sql_st)
    out = con.execute(sql_st)


def merge_into_sec_table(bucket, date_today):
    con = get_ducklake_conn()
    sql_st = f"""
    
                MERGE INTO sec AS t
                USING (
                    SELECT
                        *,
                    filename AS source_file,
                    CURRENT_TIMESTAMP AS created_at
                        
                    FROM read_parquet('s3://{bucket}/validate/{date_today}/sec_bhavdata_full.parquet')
                ) AS s
                ON (t.symbol = s.symbol AND t.series = s.series AND t.date = s.date)

                WHEN MATCHED THEN UPDATE 
                WHEN NOT MATCHED THEN INSERT ;
"""
    print(sql_st)
    out = con.execute(sql_st)
