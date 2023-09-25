from marshmallow import Schema, fields


class RecommendationSchemaOutbound(Schema):
    movie_id = fields.Str(required=True)
    movie_title = fields.Str(required=True)
    release_year = fields.Int(required=True)
    genres = fields.Str(required=True)
    director = fields.Str(required=True)
    origin = fields.Str(required=True)
    wiki_page = fields.Str(required=True)
    cast = fields.Str(required=True)
    plot = fields.Str(required=True)


class RequestSchemaInbound(Schema):
    user_id = fields.Str(required=True)


class DescriptionSchemaInbound(Schema):
    description = fields.Str(required=True)
