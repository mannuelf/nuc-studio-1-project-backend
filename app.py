import os
import csv
import xlrd
import sqlite3
import pandas as pd
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
  os.path.join(basedir, 'data/db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Init DB
ma = Marshmallow(app)  # Init Marshmallow

def db_create_population_levels():
    try:
        db_connect = sqlite3.connect('data/db.sqlite')
        cur = db_connect.cursor()

        SQL = '''CREATE TABLE population_levels (CountryID INTEGER,
                Country TEXT NOT NULL,
                Year TEXT NOT NULL,
                PRIMARY KEY (CountryID))'''

        INSERTSQL = '''INSTER INTO population_levels (CountryID, Country, Year) VALUES (?,?,?)'''
        cur.execute(SQL)
        db_connect.close()
    except sqlite3.Error as error:
        print("Failed to create database", error)
    finally:
        if db_connect:
            db_connect.close()

def db_insert_population_levels():
    try:
        db_connect = sqlite3.connect('data/db.sqlite')
        cur = db_connect.cursor()

        print("connected to db")

        SQL = '''INSERT INTO population_levels (CountryID, Country, Year) VALUES (?,?,?)'''

        population_levels_csv = open('data/factbook-2015-table1-en.csv')
        rows = csv.reader(population_levels_csv)

        cur.executemany(SQL, rows)
        print(cur.fetchall())
        db_connect.commit()
        db_connect.close()
    except sqlite3.Error as error:
        print("Failed to insert", error)
    finally:
        if db_connect:
            db_connect.close()


@app.route('/', methods=['GET'])
def get():
    db_insert_population_levels()
    # db_create() # TODO for testing create the DB, make this better.
    return jsonify({'message': 'Hello world'})


class HelloWorld(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, message, description):
        self.message = message
        self.description = description


class HelloWorldSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ('id', 'message', 'description')


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


@app.route('/hello-world/<id>', methods=['GET'])
def get_message(id):
    message = HelloWorld.query.get(id)
    result = hello_world_schema.dump(message)
    return jsonify(result)

hello_world_schema = HelloWorldSchema()
hello_worlds_schema = HelloWorldSchema(many=True)



if __name__ == '__main__':
    app.run(debug=True)
