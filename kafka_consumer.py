import json
from kafka import KafkaConsumer
from app import db

from models.session import SessionModel
# from resources.session import addUserDataToSession

LOGIN_KAFKA_TOPIC = "login_kafka_topic"

consumer = KafkaConsumer(
    LOGIN_KAFKA_TOPIC,
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    api_version=(2, 0, 2)
)

def addUserDataToSession(user_data):
    print("gggggggg" ,user_data["id"], user_data["username"])
    session = SessionModel.query.filter(SessionModel.user_id == user_data["id"]).first()
    if session:
        if session.access_token != user_data["access_token"]:
            session.username = user_data["username"], 
            session.user_id = user_data["id"],
            session.first_name = user_data["first_name"],
            session.last_name = user_data["last_name"],
            session.access_token = user_data["access_token"],
            session.refresh_token = user_data["refresh_token"]

        db.session.add(session)
        db.session.commit()
        print("session present")

        return { "message": "Session updated successfully."}, 201
    else:
        session = SessionModel(
                username = user_data["username"], 
                user_id = user_data["id"],
                first_name = user_data["first_name"],
                last_name = user_data["last_name"],
                access_token = user_data["access_token"],
                refresh_token = user_data["refresh_token"]
            )
        db.session.add(session)
        db.session.commit()
        print("session absent")

        return { "message": "Session created successfully."}, 201


while True:
    for message in consumer:
        if(message.topic == LOGIN_KAFKA_TOPIC):
            msg = message.value.decode()
            print(msg)
            addUserDataToSession(json.loads(msg))
    