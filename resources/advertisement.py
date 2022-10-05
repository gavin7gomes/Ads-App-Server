from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import AdvertisementSchema, AdvertisementUpdateSchema
from models import AdvertisementModel
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("advertisement", __name__, description="Operations on advertisements")


@blp.route("/advertisement/<int:ad_id>")
class Store(MethodView):
    @blp.response(200, AdvertisementSchema)
    def get(self, ad_id):
        advertisement = AdvertisementModel.query.get_or_404(ad_id)
        return advertisement

    def delete(self, ad_id):
        advertisement = AdvertisementModel.query.get_or_404(ad_id)
        db.session.delete(advertisement)
        db.session.commit()
        return { "message": "Advertisement successfully deleted." }

    @blp.arguments(AdvertisementUpdateSchema)
    @blp.response(200, AdvertisementSchema)
    def put(self, ad_data, ad_id):
        advertisement = AdvertisementModel.query.get(ad_id)
        if advertisement:
            advertisement.ad_name = ad_data["ad_name"]
            advertisement.ad_description = ad_data["ad_description"]
            advertisement.status = ad_data["status"]
            advertisement.media_url = ad_data["media_url"]
        else:
            advertisement = AdvertisementModel(**ad_data)
        
        db.session.add(advertisement)
        db.session.commit()

        return advertisement


@blp.route("/advertisement")
class AdvertisementList(MethodView):
    @blp.response(200, AdvertisementSchema(many=True))
    def get(self):
        return AdvertisementModel.query.all()

    @blp.arguments(AdvertisementSchema)
    @blp.response(201, AdvertisementSchema)
    def post(self, ad_data):
        advertisement = AdvertisementModel(**ad_data)
        
        try:
            db.session.add(advertisement)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message={SQLAlchemyError})

        return advertisement 