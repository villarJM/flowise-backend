from marshmallow import Schema, fields

class ProfileRegisterSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    role = fields.Str(required=True)
    company = fields.Str(required=False)
