from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST', 'PATCH'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        message_list = []
        for message in messages:
            message_list.append(message.to_dict())
        
        response = make_response(message_list, 200)
        return response
    elif request.method == 'POST':
        print(request)
        request_message = request.get_json()
        print(request_message)
        new_message = Message(request_message['body'], request_message['username'])
        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()
        print(new_message_dict)
        response = make_response(new_message_dict, 201)
        return response
    elif request.method == 'PATCH':
        response = make_response("Hello", 200)
        return response

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    
    if request.method == 'GET':
        response = make_response(message.to_dict(), 200)
        return response
    elif request.method == 'PATCH':
        request_message = request.get_json()
        if 'body' in request_message:
            message.body = request_message['body']
        if 'username' in request_message:
            message.username = request_message['username']
        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()

        response = make_response(message_dict, 200)
        return response
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Message deleted."
        }
        make_response(response_body, 200)

if __name__ == '__main__':
    app.run(port=5555)
