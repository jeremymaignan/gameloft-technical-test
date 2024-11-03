from marshmallow import Schema, fields, INCLUDE
from schemas.clan import ClanSchema
from schemas.device import DeviceSchema


class PlayerSchema(Schema):
    class Meta:
        # This allows for unknown fields to be included
        unknown = INCLUDE

    player_id = fields.Str(required=True)
    credential = fields.Str(required=True)
    created = fields.DateTime(required=True)
    modified = fields.DateTime(required=True)
    last_session = fields.DateTime(required=True)
    total_spent = fields.Int(required=True)
    total_refund = fields.Int(required=True)
    total_transactions = fields.Int(required=True)
    last_purchase = fields.DateTime(required=True)
    active_campaigns = fields.List(fields.Str(), required=True)
    devices = fields.List(fields.Nested(DeviceSchema), required=True)
    level = fields.Int(required=True)
    xp = fields.Int(required=True)
    total_playtime = fields.Int(required=True)
    country = fields.Str(required=True)
    language = fields.Str(required=True)
    birthdate = fields.DateTime(required=True)
    gender = fields.Str(required=True)
    inventory = fields.Dict(keys=fields.Str(), values=fields.Int(), required=True)
    clan = fields.Nested(ClanSchema, required=True)
