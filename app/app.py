import os
import sys
import yaml
import logging
from pathlib import Path

from flask import Flask, render_template
from flask_smorest import Api
from db_provider import db_init

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(message)s",
)


FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

CONFIG = yaml.safe_load(open(os.path.join(ROOT, "config.yml"), encoding="utf-8"))

# check if ChromaDb is provided
db_init.getOrCreateChromaDb()

from api_impl.endpoints import blp as MovieRequestBlueprint


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
        return render_template("index.html")

    @app.route("/apidocs.html")
    def apidocs():
        return render_template("apidocs.html")

    return app
