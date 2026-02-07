"""Parquet storage utilities.

Provides a thin wrapper to persist scraped tweets to a Parquet file using
`pyarrow`. The function expects a list-of-dicts that can be converted to a
pandas DataFrame.
"""

import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa


def save_parquet(tweets, file_path="tweets.parquet"):
    """Persist `tweets` to a Parquet file.

    Args:
        tweets (list): List of dictionaries representing tweet records.
        file_path (str): Destination file path.
    """
    table = pa.Table.from_pandas(pd.DataFrame(tweets))
    pq.write_table(table, file_path)