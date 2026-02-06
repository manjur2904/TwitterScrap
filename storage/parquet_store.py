import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

def save_parquet(tweets, file_path="tweets.parquet"):
    table = pa.Table.from_pandas(pd.DataFrame(tweets))
    pq.write_table(table, file_path)