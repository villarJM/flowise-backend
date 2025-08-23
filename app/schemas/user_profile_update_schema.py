from marshmallow import Schema, fields, validate

class UserProfileUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, error="Name cannot be empty"))
    last_name = fields.Str(validate=validate.Length(min=1, error="Last name cannot be empty"))
    role = fields.Str(validate=validate.Length(min=1, error="Role cannot be empty"))
    company = fields.Str()