from dotenv import find_dotenv, load_dotenv
from sentence_transformers import SentenceTransformer

import pandas as pd
import numpy as np
import dask.dataframe as dd

load_dotenv(find_dotenv(), override=True)

model = SentenceTransformer("baai/bge-large-en-v1.5")

# movie_df = pd.read_parquet("./data/movies.parquet")

# Convert the Pandas DataFrame to a Dask DataFrame
ddf = dd.read_parquet(
    "./data/movies.parquet"  # , npartitions=5
)  # 'npartitions' defines how many partitions to split the data into.


# Define a function to apply row-wise
def my_function(row):
    model.encode(row.Plot)


# Use map_partitions with Pandas' apply to apply the function row-wise
ddf.map_partitions(lambda df: df.apply(my_function, axis=1)).compute()
