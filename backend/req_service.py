from langchain.vectorstores import Chroma
from utils import _get_embedding_model
import numpy as np
import chromadb
import os
import yaml

current_path = os.path.abspath(__file__)
config_file_path = os.path.abspath(os.path.join(current_path, "..", "..", "config.yml"))
CONFIG = yaml.safe_load(open(config_file_path, encoding="utf-8"))


model = _get_embedding_model()

client = chromadb.PersistentClient(CONFIG["ChromaDBPath"])

movies_chroma = Chroma(
    client=client,
    collection_name="movies",
    embedding_function=model,
)

users_chroma = Chroma(
    client=client,
    collection_name="users",
    embedding_function=model,
)


def get_suggestion_for_user(user_id: int) -> dict:
    """Find a movie for an existing user by looking for
        similar movie embeddings

    Args:
        user_id (int): user_id

    Returns:
        dict: suggested movie

    Example:
            {'Cast': 'Jim Brown, Isaac Hayes, Bernie Casey',
            'Director': 'Keenen Ivory Wayans',
            'Origin/Ethnicity': 'American',
            'Release Year': 1988,
            'Title': "i'm gonna git you sucka",
            'Wiki Page': 'https://en.wikipedia.org/wiki/I%27m_Gonna_Git_You_Sucka',
            'genres': 'Action|Comedy',
            'movieId': '4066'}
    """

    user_data = users_chroma.get(ids=user_id, include=["embeddings"])

    if not user_data["ids"]:
        return {}

    user_embedding = user_data["embeddings"]

    movie_data = movies_chroma.similarity_search_by_vector_with_relevance_scores(
        user_embedding[0], k=1
    )[0][0]

    return prepare_response(movie_data)


def get_suggestion_general() -> dict:
    """Find a movie for a random recommendation request, here we use simply the average of all
        user embeddings and find a similar movie with some randomness attached

    Returns:
        dict: suggested movie
    """

    all_embeddings = users_chroma.get(include=["embeddings"])["embeddings"]
    avg_embedding = np.average(all_embeddings, axis=0).tolist()

    movie_data = movies_chroma.similarity_search_by_vector_with_relevance_scores(
        avg_embedding, k=5
    )

    movie_idx = np.random.choice(range(5))

    movie_data = movie_data[movie_idx][0]

    return prepare_response(movie_data)


def get_suggestion_by_description(description: str) -> dict:
    """Retuns a movie using some description provided by the user

    Args:
        description (str): movie description entered e.g. in gradio app

    Returns:
        dict: movie
    """

    embedding = _get_embedding_model().embed_query(description)

    movie_data = movies_chroma.similarity_search_by_vector(embedding, k=1)[0]

    return prepare_response(movie_data)


def prepare_response(movie_data):
    """prepares movie_data to hand back to api caller by attaching first 150 chars of movie plot

    Args:
        movie_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    response = dict(movie_data.metadata)
    response |= {"plot": f"{movie_data.page_content[:250]}..."}

    return response
