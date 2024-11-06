from marshmallow import INCLUDE, Schema, fields, validate

from schemas.clan import ClanSchema
from schemas.device import DeviceSchema


class PlayerSchema(Schema):
    class Meta:
        # This allows for unknown fields to be included
        unknown = INCLUDE

    player_id = fields.UUID(required=True)
    credential = fields.Str(required=True)
    created = fields.DateTime(required=True, format="%Y-%m-%d %H:%M:%SZ")
    modified = fields.DateTime(required=True, format="%Y-%m-%d %H:%M:%SZ")
    last_session = fields.DateTime(required=True, format="%Y-%m-%d %H:%M:%SZ")
    total_spent = fields.Int(required=True)
    total_refund = fields.Int(required=True)
    total_transactions = fields.Int(required=True)
    last_purchase = fields.DateTime(format="%Y-%m-%d %H:%M:%SZ")
    active_campaigns = fields.List(fields.Str())
    devices = fields.List(fields.Nested(DeviceSchema))
    level = fields.Int(required=True, validate=validate.Range(min=1))
    xp = fields.Int(required=True)
    total_playtime = fields.Int(required=True)
    country = fields.Str(required=True, validate=validate.OneOf(["US", "CA", "RO", "FR"]))
    language = fields.Str(required=True, validate=validate.OneOf(["fr", "en"]))
    birthdate = fields.DateTime(required=True, format="%Y-%m-%d %H:%M:%SZ")
    gender = fields.Str(required=True, validate=validate.OneOf(["male", "female", "other"]))
    inventory = fields.Dict(required=True, keys=fields.Str(), values=fields.Int())
    clan = fields.Nested(ClanSchema)
