from flask.views import MethodView
from flask_smorest import Blueprint, abort
from recommender import (
    get_suggestion_for_user,
    get_suggestion_general,
    get_suggestion_by_description,
)
from app.api_impl.schemas import (
    RecommendationSchemaOutbound,
    RequestSchemaInbound,
    DescriptionSchemaInbound,
)

blp = Blueprint(
    "Movie Requests",
    "movie_requests",
    description="Description of Movie Recommender REST API endpoints",
)

# TODO: RequestSchemaInbound is deactivated for now, can be used
# to further add information to the request and find a better movie


@blp.route("/api/rec_by_userid/<string:user_id>")
class MovieRequestForUser(MethodView):
    # @blp.arguments(RequestSchemaInbound)
    @blp.response(200, RecommendationSchemaOutbound)
    def get(self, user_id):
        # if request_data["user_id"] != user_id:
        #    abort(404, message="Invalid api call.")
        # find movie based on user history
        movie_data = get_suggestion_for_user(user_id)

        # no user_id in db if movie_data dict is empty
        if not movie_data:
            abort(404, message=f"No user found for id {user_id}.")

        return prepare_result(movie_data)


@blp.route("/api/rec")
class MovieRequestGeneral(MethodView):
    # @blp.arguments(RequestSchemaInbound)
    @blp.response(200, RecommendationSchemaOutbound)
    def get(self):
        movie_data = get_suggestion_general()

        if not movie_data:
            abort(404, message="Something went wrong.")

        return prepare_result(movie_data)


@blp.route("/api/rec_by_descr")
class MovieRequestByDescription(MethodView):
    @blp.arguments(DescriptionSchemaInbound)
    @blp.response(200, RecommendationSchemaOutbound)
    def get(self, request_data):
        movie_data = get_suggestion_by_description(request_data["description"])

        if not movie_data:
            abort(404, message="Something went wrong.")

        return prepare_result(movie_data)


# TODO: the movies.csv column names are returned here as keys
# and should be changed to adhere to API specs in schemas.py
def prepare_result(movie_data: dict) -> dict:
    new_keys = [
        "cast",
        "director",
        "origin",
        "release_year",
        "movie_title",
        "wiki_page",
        "genres",
        "movie_id",
        "plot",
    ]
    old_keys = movie_data.keys()
    key_mapping = dict(zip(old_keys, new_keys))

    # Create a new dictionary with the updated keys
    new_data = {key_mapping.get(k): v for k, v in movie_data.items()}

    return new_data
