from datetime import datetime
import enum
from db import db

class StatusEnums(str, enum.Enum):
    PUBLISHED = "PUBLISHED"
    UNPUBLISHED = "UNPUBLISHED"

class AdvertisementModel(db.Model):
    __tablename__ = 'advertisement'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    ad_name = db.Column(db.String(120), nullable=False)
    ad_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    status = db.Column(
        db.Enum(StatusEnums), default=StatusEnums.PUBLISHED, nullable=False
    )
    media_url = db.Column(db.String(255), nullable=False)
    products = db.relationship("ProductModel", back_populates="advertisement")