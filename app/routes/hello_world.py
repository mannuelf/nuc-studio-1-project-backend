from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

db = SQLAlchemy(app)  # Init DB
ma = Marshmallow(app)  # Init Marshmallow


@app.route('/hello-world', methods=['POST'])
def add_message():
    message = request.json['message']
    description = request.json['description']

    new_message = HelloWorld(message, description)

    db.session.add(new_message)
    db.session.commit()

    return hello_world_schema.jsonify(new_message)


@app.route('/hello-world', methods=['GET'])
def get_messages():
    all_messages = HelloWorld.query.all()
    result = hello_worlds_schema.dump(all_messages)
    return jsonify(result)


# Get one message
@app.route('/hello-world/<id>', methods=['GET'])
def get_message(id):
    message = HelloWorld.query.get(id)
    result = hello_world_schema.dump(message)
    return jsonify(result)
