from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models.session import SessionModel
from schemas import SessionSchema


blp = Blueprint("session", __name__, description="Operations on Sessions")


@blp.route("/session/<int:session_id>")
class Product(MethodView):
    @blp.response(200, SessionModel)
    def get(self, session_id):
        sess = SessionModel.query.get_or_404(session_id)
        return sess

    def delete(self, session_id):
        sess = SessionModel.query.get_or_404(session_id)
        db.session.delete(sess)
        db.session.commit()
        return { "message": "Session successfully deleted." }

    @blp.arguments(SessionModel)
    @blp.response(200, SessionModel)
    def put(self, session_data, session_id):
        session = SessionModel.query.filter(SessionModel.id == session_id).first()
        if session:
            session.username = session_data["username"], 
            session.user_id = session_data["user_id"],
            session.first_name = session_data["first_name"],
            session.last_name = session_data["last_name"],
            session.access_token = session_data["access_token"],
            session.refresh_token = session_data["refresh_token"]

            db.session.add(session)
            db.session.commit()
            return session
        else:
            return { "message": "Session not found." }


@blp.route("/session")
class SessionList(MethodView):
    @blp.response(200, SessionSchema(many=True))
    def get(self):
        return SessionModel.query.all()

    @blp.arguments(SessionSchema)
    @blp.response(201, SessionSchema)
    def post(self, session_data):
        sess = SessionModel(**session_data)
        
        try:
            db.session.add(sess)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message={SQLAlchemyError})

        return sess
