from marshmallow import Schema, fields, validate

commands = ('filter', 'map', 'unique', 'sort', 'limit', 'regex')


class RequestSchema(Schema):

    cmd = fields.Str(required=True, validate=validate.OneOf(commands))
    value = fields.Str(required=True)


class BatchRequestSchema(Schema):
    queries = fields.Nested(RequestSchema, many=True)
    file_name = fields.Str(required=True)
