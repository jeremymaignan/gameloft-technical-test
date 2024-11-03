from marshmallow import Schema, fields

class DeviceSchema(Schema):
    id = fields.Int(required=True)
    model = fields.Str(required=True)
    carrier = fields.Str(required=True)
    firmware = fields.Str(required=True)
