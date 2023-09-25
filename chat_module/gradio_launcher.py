import sys
import os
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
print(ROOT)
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import gradio as gr


def get_movie(input):
    import json
    import requests

    # Define the JSON data
    params = dict(description=input)

    # Make the GET request with the JSON data in the body
    # Note: This is non-standard and might not be correctly handled by all servers
    FLASK_HOST = os.environ.get("FLASK_HOST")
    FLASK_PORT = os.environ.get("FLASK_PORT")

    response = requests.get(
        url=f"http://{FLASK_HOST}:{FLASK_PORT}/api/rec_by_descr",
        json=params,
    )

    response_data = dict(response.json())

    result = f"Title: {response_data['movie_title']}\n\
MovieId: {response_data['movie_id']}\n\
Year: {response_data['release_year']}\n\
Origin: {response_data['origin']}\n\
Director: {response_data['director']}\n\
Cast: {response_data['cast']}\n\
Genre: {response_data['genres']}\n\
Wiki: {response_data['wiki_page']}\n\n\
Plot: {response_data['plot']}"

    return result


# Create your gradio Interface
iface = gr.Interface(
    fn=get_movie,
    inputs=gr.inputs.Textbox(lines=7, label="Enter a movie description here."),
    outputs="text",
)


# Launches Gradio App
iface.launch(server_name="0.0.0.0", share=False)
