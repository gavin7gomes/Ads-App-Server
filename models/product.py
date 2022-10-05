from datetime import datetime
from enum import unique
from db import db
from models import AdvertisementModel


class ProductModel(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    product_name = db.Column(db.String(120), nullable=False)
    product_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    price = db.Column(db.Float, default=0, nullable=False)
    in_stock = db.Column(db.Integer, default=0, nullable=False)
    media_url = db.Column(db.String(255), nullable=False)
    ad_id = db.Column(db.Integer, db.ForeignKey("advertisement.id"), nullable=False, unique=False)
    advertisement = db.relationship("AdvertisementModel", back_populates="products")