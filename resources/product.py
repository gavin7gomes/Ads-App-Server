from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models.product import ProductModel
from schemas import PlainProductSchema, ProductSchema, ProductUpdateSchema


blp = Blueprint("product", __name__, description="Operations on Products")


@blp.route("/product/<int:product_id>")
class Product(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        return product

    def delete(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return { "message": "Product successfully deleted." }

    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, ProductSchema)
    def put(self, product_data, product_id):
        product = ProductModel.query.get(product_id)
        if product:
            product.product_name = product_data["product_name"]
            product.product_description = product_data["product_description"]
            product.price = product_data["price"]
            product.in_stock = product_data["in_stock"]
            product.media_url = product_data["media_url"]
            product.ad_id = product_data["ad_id"]
        else:
            product = ProductModel(**product_data)
        
        db.session.add(product)
        db.session.commit()

        return product


@blp.route("/product")
class ProductList(MethodView):
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        return ProductModel.query.all()

    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        item = ProductModel(**product_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message={e})

        return item

