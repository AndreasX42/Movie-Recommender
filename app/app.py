import os
import logging

from flask import Flask, render_template
from flask_smorest import Api
from app.api_impl import MovieRequestBlueprint

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(message)s",
)


def create_app():
    app = Flask(__name__)
    app.config["API_TITLE"] = "REST API Docs"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)
    api.register_blueprint(MovieRequestBlueprint)

    @app.route("/")
    def home():
        return render_template(
            "index.html",
            localhost_port=os.environ.get("LOCALHOST_PORT"),
            gradio_port=os.environ.get("GRADIO_PORT"),
        )

    return app
