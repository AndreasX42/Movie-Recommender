import pandas as pd

movie_df = pd.read_csv("./data/movies.csv")
movie_df.to_parquet("./data/movies.parquet")
