from langchain.vectorstores import Chroma
from utils.helper import _get_embedding_model
from app.db_provider.db import client
import numpy as np

model = _get_embedding_model()

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
    )[0][0].metadata

    return movie_data


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

    return movie_data[movie_idx][0].metadata
