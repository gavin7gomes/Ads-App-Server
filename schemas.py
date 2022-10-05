from marshmallow import Schema, fields

from models import advertisement


class PlainAdvertisementSchema(Schema):
    id = fields.Int(dump_only=True)
    ad_name = fields.Str(required=True)
    ad_description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    status = fields.Str()
    media_url = fields.Str()


class AdvertisementUpdateSchema(Schema):
    ad_name = fields.Str(required=True)
    ad_description = fields.Str()
    status = fields.Str()
    media_url = fields.Str()


class PlainProductSchema(Schema):
    id = fields.Int(dump_only=True)
    product_name = fields.Str(required=True)
    product_description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    price = fields.Float(required=True)
    in_stock = fields.Integer(required=True)
    media_url = fields.String()


class ProductUpdateSchema(Schema):
    product_name = fields.Str(required=True)
    product_description = fields.Str()
    price = fields.Float(required=True)
    in_stock = fields.Integer(required=True)
    media_url = fields.String()
    ad_id = fields.Int()


class ProductSchema(PlainProductSchema):
    ad_id = fields.Int(required=True, load_only=True)
    advertisement = fields.Nested(PlainAdvertisementSchema, dump_only=True)


class AdvertisementSchema(PlainAdvertisementSchema):
    products = fields.List(fields.Nested(PlainProductSchema()), dump_only=True)
