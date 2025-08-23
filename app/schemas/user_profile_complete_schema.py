from marshmallow import Schema, fields, validate

class UserProfileCompleteSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, error="Name cannot be empty"))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, error="Last name cannot be empty"))
    role = fields.Str(required=True, validate=validate.Length(min=1, error="Role cannot be empty"))
    company = fields.Str(required=False)
