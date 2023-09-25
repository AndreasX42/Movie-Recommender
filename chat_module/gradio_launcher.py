import os
import requests
import gradio as gr


def get_movie(input):
    # Define the JSON data payload
    params = dict(description=input)

    # make the GET request with the JSON data in the body
    FLASK_HOST = os.environ.get("FLASK_HOST")
    FLASK_PORT = os.environ.get("FLASK_PORT")

    response = requests.get(
        url=f"http://{FLASK_HOST}:{FLASK_PORT}/api/req_by_descr",
        json=params,
    )

    # pretify the data before serving
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


# create the gradio Interface
iface = gr.Interface(
    fn=get_movie,
    inputs=gr.inputs.Textbox(lines=7, label="Enter a movie description here."),
    outputs="text",
)


# launches Gradio App
iface.launch(server_name="0.0.0.0", share=False)
