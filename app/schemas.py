from marshmallow import Schema, fields


class SportSchema(Schema):
    name = fields.Str(load_only=True)
    slug = fields.Str(required=True)
    active = fields.Boolean(required=True)


class SportUpdateSchema(Schema):
    slug = fields.Str()
    active = fields.Boolean()


class EventSchema(Schema):
    name = fields.Str(required=True)
    slug = fields.Str(required=True)
    active = fields.Boolean(required=True)
    type = fields.Str(required=True)
    sport = fields.Str(required=True)
    status = fields.Str(required=True)
    scheduled_start = fields.DateTime(required=True)
    actual_start = fields.DateTime()


class SelectionSchema(Schema):
    name = fields.Str(required=True)
    event = fields.Str(required=True)
    price = fields.Float(required=True)
    active = fields.Boolean(required=True)
    outcome = fields.Str(required=True)


class SelectionUpdateSchema(Schema):
    name = fields.Str(load_only=True)
    event = fields.Str(load_only=True)
    price = fields.Float()
    active = fields.Boolean()
    outcome = fields.Str()
