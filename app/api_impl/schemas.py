from marshmallow import Schema, fields


class RecommendationSchemaOutbound(Schema):
    # id = fields.Str(required=False)
    # movie_name = fields.Str(required=True)
    # release_year = fields.Str(required=True)
    # genres = fields.Str(required=True)
    # plot = fields.Str(required=True)
    movie_description = fields.Str(required=True)
    message1 = fields.Str(required=True)
    message2 = fields.Str(required=True)


class RequestSchemaInbound(Schema):
    movie_description = fields.Str(required=True)
