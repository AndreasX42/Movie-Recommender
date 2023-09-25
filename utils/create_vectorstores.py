from tqdm.auto import tqdm
import pandas as pd
import chromadb
import yaml
import logging
import os

from utils.helper import _calculate_average_embedding, _get_embedding_model

current_path = os.path.abspath(__file__)
config_file_path = os.path.abspath(os.path.join(current_path, "..", "..", "config.yml"))
CONFIG = yaml.safe_load(open(config_file_path, encoding="utf-8"))


def create_chromadb():
    """creates chromadb with movies and users collections"""
    _create_movie_collection()
    _create_user_collection()


def _create_movie_collection() -> None:
    """_summary_

    Args:
        model (HuggingFaceEmbeddings): _description_
    """

    logging.info("Creating vectorstore for movies. This can take some time.")

    client = chromadb.PersistentClient(path=CONFIG["ChromaDBPath"])
    movie_collection = client.create_collection(
        "movies", metadata={"hnsw:space": "cosine"}
    )

    model = _get_embedding_model()

    # movies data preprocessing
    movie_df = pd.read_csv(CONFIG["MovieCsv"])
    COLS = [
        "movieId",
        "Title",
        "Release Year",
        "Origin/Ethnicity",
        "Director",
        "Cast",
        "genres",
        "Wiki Page",
        "Plot",
    ]
    movie_df = movie_df[COLS]
    movie_df["movieId"] = movie_df["movieId"].astype(int).astype(str)
    movie_df["Cast"] = movie_df["Cast"].fillna("Unknown")

    # create collection in chromadb
    # we will use batches of 64
    batch_size = 8

    for i in tqdm(range(0, len(movie_df), batch_size)):
        # find end of batch
        i_end = min(i + batch_size, len(movie_df))

        # extract batch
        batch = movie_df.iloc[i:i_end]

        # generate embeddings for batch, every row gets transformed into string and encoded
        embeddings = model.embed_documents(batch["Plot"].tolist())

        # get metadata and documents
        meta = batch.drop("Plot", axis=1).to_dict(orient="records")
        docs = batch["Plot"].tolist()

        # create IDs
        ids = batch["movieId"].values.tolist()

        # add all to upsert list
        movie_collection.upsert(
            ids=ids, embeddings=embeddings, metadatas=meta, documents=docs
        )


def _create_user_collection() -> None:
    """_summary_

    Args:
        model (HuggingFaceEmbeddings): _description_
    """

    logging.info("Creating vectorstore for users. This can take some time.")

    # preprocess user data
    users_df = pd.read_csv(CONFIG["UserCsv"])
    COLS = ["userId", "movieId", "timestamp"]
    users_df = users_df[COLS]
    users_df["userId"] = users_df["userId"].astype(str)
    users_df["movieId"] = users_df["movieId"].astype(str)

    # load chromadb client and collections
    client = chromadb.PersistentClient(path=CONFIG["ChromaDBPath"])
    movie_collection = client.get_collection("movies")
    user_collection = client.get_or_create_collection(
        "users", metadata={"hnsw:space": "cosine"}
    )

    for userId in tqdm(users_df.userId.unique()):
        user_data = users_df[users_df.userId == userId]

        # find all movieId and timestamps pairs of user
        timestamps = user_data.timestamp.to_numpy()
        movieIds = user_data.movieId.tolist()

        # get exponential moving average of corresponding embeddings wrt timestamps
        embedding = _calculate_average_embedding(
            movieIds, timestamps, movie_collection
        ).tolist()

        # get metadata and documents
        meta = {
            "userId": userId,
            "movieIds": str(movieIds),
            "timestamps": str(timestamps),
        }

        # create IDs
        ids = userId

        # add all to upsert list
        user_collection.upsert(ids=ids, embeddings=embedding, metadatas=meta)
