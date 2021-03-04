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
  os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Init DB
ma = Marshmallow(app)  # Init Marshmallow

def db_create():
    db_connect = sqlite3.connect('./db.sqlite')
    connect = db_connect.cursor()

    # Population Levels
    pl_data = pd.read_csv('data/factbook-2015-table1-en.csv')
    SQL = '''CREATE TABLE population_levels (CountryID INTEGER,
                Country TEXT NOT NULL,
                Year TEXT NOT NULL,
                PRIMARY KEY (CountryID))'''
    INSERTSQL = '''INSTER INTO population_levels (CountryID, Country, Year) VALUES (?,?,?)'''
    #connect.execute(SQL)
    with open(pl_data, 'r') as csvfile:
      reader = csv.reader(csvfile)
      next(reader) # skip header
      for row in reader:
        print(row)
      connect.close()


@app.route('/', methods=['GET'])
def get():
    db_create() # for testing create the DB, TODO make this better.
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

class PopulationLevels(db.Model):
  __tablename__ = "population_levels"
  CountryId = Column(Integer, primary_key=True)
  Country = Column(String)
  Year = Column(String)

class PopulationLevelsSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ('CountryId', 'Country', 'Year')

@app.route('/population-levels', method=['GET'])
def get_population_levels():
  print("getting population levels")
  data = PopulationLevels.query.get()
  result = population_levels_schema.dump(data)
  return jsonify(result)

# Init the schema
hello_world_schema = HelloWorldSchema()
hello_worlds_schema = HelloWorldSchema(many=True)
population_levels_schema = PopulationLevelsSchema()
population_levels_schema = PopulationLevelsSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)
