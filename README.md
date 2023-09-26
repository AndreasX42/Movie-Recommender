# Movie-Recommender
Implementation of a simple movie recommender using embedding models, ChromaDb, LangChain and Flask API.

## Overview

We take the dataset of movies and build a ChromaDB vectorstore from the embeddings of the movie descriptions. For every user we take the watch history and calculate an average of the embeddings
of the movies watched in the past to provide a recommendation. Additionally on the Flask frontend we provide a simple Gradio app where one can enter some description of what movie they want
to watch and serve some suggestion.

## Directory Structure 📂

- `app`: Handles the frontend with Flask.
- `backend`: Contains everything needed to set up ChromaDB and provide recommendations, including a Flask API.
- `chat_module`: Script for starting the Gradio app.
- `data`: Directory for datasets.
- `notebooks`: Some jupyter notebooks for experiments.

## Setup 👨‍💻

We run the app by starting up three docker containers, one for the frontend 'app', one for the Gradio chat module and one for the backend that also manages the API requests.
The command for this is simply 'docker-compose up (--build)'. A documentation for the API is provided at 'localhost:5055/swagger-ui'.

## Frontend 🔥

![imagen](https://github.com/AndreasX42/Movie-Recommender/assets/141482745/62157e1a-671a-4d40-bb89-e4b0f7e956f5)
