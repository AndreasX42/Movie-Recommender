from langchain.embeddings import HuggingFaceEmbeddings
import numpy as np
import chromadb
import yaml
import os

current_path = os.path.abspath(__file__)
config_file_path = os.path.abspath(os.path.join(current_path, "..", "..", "config.yml"))
CONFIG = yaml.safe_load(open(config_file_path, encoding="utf-8"))


def _get_embedding_model() -> HuggingFaceEmbeddings:
    """Getter for the embedding model

    Returns:
        HuggingFaceEmbeddings: the embedding model
    """

    model = HuggingFaceEmbeddings(
        model_name=CONFIG["EmbeddingModel"],
        model_kwargs={"device": CONFIG["EmbeddingDevice"]},  # "cuda"
        encode_kwargs={"normalize_embeddings": CONFIG["EmbeddingNormalized"]},
    )

    return model


def _calculate_average_embedding(
    movie_ids: list[str],
    timestamps: list[int],
    movie_collection: chromadb.api.models.Collection,
) -> np.ndarray:
    """Calculates a weighted embedding of all the movies the user watched
        with exponential weights regarding timestamps

    Args:
        movieIds (list[str]): _description_
        timestamps (list[int]): _description_
        movie_collection (_type_): _description_

    Returns:
        _type_: _description_
    """

    max_timestamp = max(timestamps)
    decay_factor = 0.1  # You can adjust the decay factor as needed
    weights = np.exp(decay_factor * (np.array(timestamps) - max_timestamp))

    # Normalize the weights so that they sum up to 1
    weights = weights / weights.sum()
    weights = weights.reshape(-1, 1)

    # Calculate the weighted average of the vectors
    embeddings = np.array(
        movie_collection.get(ids=movie_ids, include=["embeddings"])["embeddings"]
    ).reshape(CONFIG["EmbeddingDim"], -1)
    weighted_embedding = embeddings @ weights

    return weighted_embedding.flatten()
