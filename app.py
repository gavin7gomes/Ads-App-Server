import json
import os
from uuid import uuid4
from flask import Flask, request
from flask_smorest import abort, Api
from db import db
import models
from resources.advertisement import blp as AdvertisementBlueprint
from resources.product import blp as ProductBlueprint

from kafka import KafkaConsumer


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdeliv.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv( "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(AdvertisementBlueprint)
    api.register_blueprint(ProductBlueprint)

    return app

if __name__ == '__main__':
    SAMPLE_KAFKA_TOPIC = "sample_topic"
    consumer = KafkaConsumer(
        SAMPLE_KAFKA_TOPIC,
        bootstrap_servers='192.168.2.8:29092',
        auto_offset_reset='earliest',
        api_version=(2, 0, 2)
    )

    while True:
        for message in consumer:
            print(json.loads(message.value.decode()))