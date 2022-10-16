import json
import os
from flask import Flask, request
from flask_smorest import abort, Api
from db import db
import models
from kafka import KafkaConsumer
from flask_cors import CORS, cross_origin

from resources.advertisement import blp as AdvertisementBlueprint
from resources.product import blp as ProductBlueprint
from resources.session import blp as SessionBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Ads REST API"
app.config["API_VERSION"] = "v1.0"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdeliv.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.app = app
db.init_app(app)
CORS(app, support_credentials=True)

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.register_blueprint(AdvertisementBlueprint)
api.register_blueprint(ProductBlueprint)
api.register_blueprint(SessionBlueprint)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)