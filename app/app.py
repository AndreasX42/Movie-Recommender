import os
import logging
from flask import Flask, render_template

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(message)s",
)


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template(
            "index.html",
            localhost_api_port=os.environ.get("LOCALHOST_API_PORT"),
            gradio_port=os.environ.get("GRADIO_PORT"),
        )

    return app
