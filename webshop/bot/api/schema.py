from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(validate=validate.Length(min=2, max=512), required=True)
    description = fields.String(validate=validate.Length(min=8, max=2048))
    subcategories = fields.List(fields.String)
    parent = fields.String()


class ProductSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(validate=validate.Length(min=2, max=512), required=True)
    description = fields.String(validate=validate.Length(min=8, max=2048))
    in_stock = fields.String(validate=validate.Length(min=0), required=True)
    is_available = fields.Boolean()
    discount = fields.Integer(validate=validate.Length(min=0, max=100))
    price = fields.Decimal(validate=validate.Length(min=1))
    image = fields.String(dump_only=True)
    parameter = fields.String()
    category = fields.String()


class UserSchema(Schema):
    id = fields.String(dump_only=True)
    user_id = fields.String(required=True)
    first_name = fields.String(required=True)
    second_name = fields.String()
    username = fields.String(required=True)
    language_code = fields.String(required=True)
    prone_number = fields.Integer()


class OrderSchema(Schema):
    id = fields.String(dump_only=True)
    customer = fields.String()
    products = fields.List(fields.String)
    date = fields.DateTime()

