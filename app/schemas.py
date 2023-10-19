from marshmallow import Schema, fields


class SportSchema(Schema):
    name = fields.Str(load_only=True)
    slug = fields.Str(required=True)
    active = fields.Boolean(required=True)


class EventSchema(Schema):
    name = fields.Str(required=True)
    slug = fields.Str(required=True)
    active = fields.Boolean(required=True)
    type = fields.Str(required=True)
    sport = fields.Str(required=True)
    scheduled_start = fields.DateTime(required=True)
    actual_start = fields.DateTime()
