from marshmallow import Schema, fields


class ClanSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
