from flask.views import MethodView
from flask_smorest import Blueprint, abort

from api_impl.schemas import RecommendationSchemaOutbound, RequestSchemaInbound
from db_provider.db import client, movie_collection, user_collection

blp = Blueprint(
    "Movie Requests",
    "movie_requests",
    description="Description of Movie Recommender REST API endpoints",
)


@blp.route("/get_new_user_recommendation/<string:user_id>")
class MovieRequestForUser(MethodView):
    @blp.arguments(RequestSchemaInbound)
    @blp.response(200, RecommendationSchemaOutbound)
    def get(self, request_data, user_id):
        try:
            return {
                "movie_description": request_data["movie_description"],
                "message1": user_collection.get(ids=user_id)["metadatas"][0]["userId"],
                "message2": movie_collection.get(ids="1")["metadatas"],
            }
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/get_new_user_recommendation")
class MovieRequestGeneral(MethodView):
    @blp.arguments(RequestSchemaInbound)
    @blp.response(200, RecommendationSchemaOutbound)
    def get(self, request_data):
        print("the input was: ", request_data)
        try:
            return {
                "movie_description": request_data["movie_description"],
                "message2": movie_collection.get(ids="1")["metadatas"],
            }
        except KeyError:
            abort(404, message="Item not found.")
