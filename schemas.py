from marshmallow import Schema, fields


class StudentSchema(Schema):
    first_name = fields.Str(required=True, validate=fields.Length(100))
    last_name = fields.Str(required=True)
    birth_date = fields.Date(format="%Y-%m-%d", required=True)
    group_id = fields.Int(required=True)
