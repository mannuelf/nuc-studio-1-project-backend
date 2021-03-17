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

# using SQLALchemy and sqlite3 with raw queries, we should pick one and stick to it, but for now this works.
db = SQLAlchemy(app)  # Init DB
ma = Marshmallow(app)  # Init Marshmallow


def db_create_population_levels():
    try:
        db_connect = sqlite3.connect('data/db.sqlite')
        cur = db_connect.cursor()

        SQL = '''CREATE TABLE IF NOT EXISTS population_levels (CountryID INTEGER,
                Country TEXT NOT NULL,
                [2002] TEXT NOT NULL,
                [2003] TEXT NOT NULL,
                [2004] TEXT NOT NULL,
                [2005] TEXT NOT NULL,
                [2006] TEXT NOT NULL,
                [2007] TEXT NOT NULL,
                [2008] TEXT NOT NULL,
                [2009] TEXT NOT NULL,
                [2010] TEXT NOT NULL,
                [2011] TEXT NOT NULL,
                [2012] TEXT NOT NULL,
                [2013] TEXT NOT NULL,
                [2014] TEXT NOT NULL,
                PRIMARY KEY (CountryID))'''
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

        print("🚀 connected to db")

        SQL = '''INSERT INTO population_levels (Country, Year) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        population_levels_csv = pd.read_csv('data/factbook-2015-table1-en.csv', engine='python',
                                            encoding="UTF-8", header=0, delimiter=";", skiprows=3, skipfooter=1, index_col=0)
        df_drop_last_2_rows = population_levels_csv.iloc[:-1]
        df_drop_last_2_rows.columns.values[0] = "Country"
        print(df_drop_last_2_rows)
        df_drop_last_2_rows.to_sql(
            'population_levels', db_connect, if_exists='append', index=False)
        cur.execute("SELECT * FROM population_levels")
        print("💿", cur.fetchall())
        db_connect.commit()
        db_connect.close()
    except sqlite3.Error as error:
        print("Failed to insert", error)
    finally:
        if db_connect:
            db_connect.close()


@app.route('/', methods=['GET'])
def get():
    db_create_population_levels()
    db_insert_population_levels()
    return jsonify({'message': 'Hello world'})


class PopulationLevels(db.Model):
    __tablename__ = 'population_levels'
    id = db.Column(db.Integer)
    CountryID = db.Column(db.Integer, primary_key=True)
    Country = db.Column(db.String(100), unique=True)
    year_1 = db.Column(db.String)
    year_2 = db.Column(db.String)
    year_3 = db.Column(db.String)
    year_4 = db.Column(db.String)
    year_5 = db.Column(db.String)
    year_6 = db.Column(db.String)
    year_6 = db.Column(db.String)
    year_7 = db.Column(db.String)
    year_8 = db.Column(db.String)
    year_9 = db.Column(db.String)
    year_10 = db.Column(db.String)
    year_11 = db.Column(db.String)
    year_12 = db.Column(db.String)
    year_13 = db.Column(db.String)

    def __init__(self, CountryID, Country,  year_1, year_2, year_3, year_4, year_5, year_6, year_7, year_8, year_9, year_10, year_11, year_12, year_13):
        self.CountryID = CountryID
        self.country = Country
        self.year_1 = year_1
        self.year_2 = year_2
        self.year_3 = year_3
        self.year_4 = year_4
        self.year_5 = year_5
        self.year_6 = year_6
        self.year_7 = year_7
        self.year_8 = year_8
        self.year_9 = year_9
        self.year_10 = year_10
        self.year_11 = year_11
        self.year_12 = year_12
        self.year_13 = year_13


# class PopulationLevelsSchema(ma.SQLAlchemySchema):
 #   class Meta:
  #      fields = (countryID, country,  year_1, year_2, year_3, year_4, year_5,
   #               year_6, year_7, year_8, year_9, year_10, year_11, year_12, year_13)


@app.route('/population-levels', methods=['GET'])
def get_population_levels():
    try:
        db_connect = sqlite3.connect('data/db.sqlite')
        cur = db_connect.cursor()

        print("🚀 connected to db")
        SQL = '''SELECT * FROM population_levels'''
        query = cur.execute(SQL)
        result = query.fetchall()
        db_connect.commit()
        db_connect.close()
        endpoint_obj = {}
        count = 0
        for country in result:
            count += 1
            endpoint_obj[count] = {
                "id": country[0],
                "country": country[1],
                "2002":  country[2],
                "2003": country[3],
                "2004": country[4],
                "2005": country[5],
                "2006": country[6],
                "2007": country[7],
                "2008": country[8],
                "2009": country[9],
                "2010": country[10],
                "2011": country[11],
                "2012": country[12],
                "2013": country[13],
                "2014": country[14]
            }
        return jsonify(endpoint_obj)
    except sqlite3.Error as error:
        print("💥", error)
    finally:
        if db_connect:
            db_connect.close()
            print("I am done")


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


hello_world_schema = HelloWorldSchema()
hello_worlds_schema = HelloWorldSchema(many=True)


if __name__ == '__main__':
    app.run(debug=True)
