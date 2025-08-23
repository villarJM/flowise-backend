from marshmallow import Schema, fields

class UserUpdateSchema(Schema):
    name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    company = fields.Str()