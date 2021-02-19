import os

import xlrd
import sqlite3
import pandas as pd
from . import db
from setuptools import setup
from flask import Flask, request, jsonify, g
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from models.population_levels import PopulationLevels

setup(
    name='factbookexplorers',
    packages=['factbookexplorers'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-marshmallow',
        'marshmallow-sqlalchemy',
        'pandas',
        'xlrd'
    ],
)


def create_app():
    app = Flask('__name__', instance_relative_config=True)
    from . import db
    db.init_app(app)

    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET'])
    def get():
        return jsonify({'message': 'Hello world'})

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
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

    population_levels_schema = PopulationLevels()

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

    @app.route('/population-levels', methods=['GET'])
    def get_data():
        pass

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    if __name__ == '__main__':
        app.run(debug=True)

    return app
