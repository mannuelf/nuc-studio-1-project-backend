import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pandas as pd
import sqlite3
import xlrd

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


@app.route('/', methods=['GET'])
def get():
    return jsonify({'message': 'Hello world'})


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Init DB
ma = Marshmallow(app)  # Init Marshmallow


# Hello World Class/Model
class HelloWorld(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, message, description):
        self.message = message
        self.description = description


# Hello World Schema
class HelloWorldSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ('id', 'message', 'description')


# Init the schema
hello_world_schema = HelloWorldSchema()
hello_worlds_schema = HelloWorldSchema(many=True)


# Create message
@app.route('/hello-world', methods=['POST'])
def add_message():
    message = request.json['message']
    description = request.json['description']

    new_message = HelloWorld(message, description)

    db.session.add(new_message)
    db.session.commit()

    return hello_world_schema.jsonify(new_message)


# Get all messages
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


if __name__ == '__main__':
    app.run(debug=True)
