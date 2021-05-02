import os
import csv
import xlrd
import sqlite3
import pandas as pd
from flask_cors import CORS
from flask import Flask, request, jsonify, g
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
DATABASE = 'data/db.sqlite'

# function to initialise an intance of a db connection.
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# will have remove these as we using sqlite3 

# basedir keeps reference to the location or path where the root of 
# the application is kept and running.
basedir = os.path.abspath(os.path.dirname(__file__))

# this is a SQLAlchemy database connection configuration, it should be removed.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data/db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# using SQLALchemy and sqlite3 with raw queries, we should pick one and stick to it, but for now this works.
db = SQLAlchemy(app)  # Init DB
ma = Marshmallow(app)  # Init Marshmallow


def db_create_gross_gdp():
    """
    Creates a table called gross_gdp. This is the just make it work version...
    we should create migrations, using https://flask-migrate.readthedocs.io/en/latest/
    but we can do later I just want to get things working.
    to initiate this function I simply call it using the home route function I 
    call db_create_gross_gdp() inside home route and it does its job once.
    """
    try:
        cur = get_db().cursor()
        SQL = '''CREATE TABLE IF NOT EXISTS gross_gdp (CountryID INTEGER,
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
        cur.close()
    except sqlite3.Error as error:
        print("Failed to create database", error)
    finally:
        print("complete")


def db_insert_gross_gdp():
    """
    Gross GDP data insert
    This function again I call it on the home route function and this function 
    inserts all the data gotten from the CSV.
    after calling it once, i remove the function call from the homeroute call, 
    we need to create database migration using https://flask-migrate.readthedocs.io/en/latest/
    """
    try:
        with app.app_context():
            cur = get_db()

            gross_gdp_csv = pd.read_csv('data/gross-gdp.csv', engine='python',
                                        encoding="UTF-8", header=0, delimiter=";",
                                        skiprows=3, skipfooter=1, index_col=0)

            df_drop_last_2_rows = gross_gdp_csv.iloc[:-1]
            df_drop_last_2_rows.columns.values[0] = "Country"
            df_drop_last_2_rows.to_sql('gross_gdp', cur, if_exists='append', index=False)
            cur.close()
    except sqlite3.Error as error:
        print("Failed to insert", error)
    finally:
        print("complete")

# ApiSpec https://apispec.readthedocs.io/en/latest/
@app.route('/gross-gdp', methods=['GET'])
def get_gross_gdp():
    """ A endpoint to retreive gross gdp levels data per country.
    ---
    get:
      description: Get all gross gdp level data.
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: Return a collection of countries and their gross gdp figures per year.
          content:
            application/json:
              schema: GrossGdpSchema
    """
    try:
        cur = get_db().cursor()
        table_name = 'gross_gdp'
        result = cur.execute("""SELECT * FROM gross_gdp""").fetchall()
        cur.close()

        endpoint_obj = {}
        count = 0
        for country in result:
            count += 1
            endpoint_obj[country[1].lower().replace(" ", "-")] = {
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
        if cur:
            cur.close()
            print("closing db")



def db_create_population_levels():
    try:
        cur = get_db().cursor()

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
        cur.close()
    except sqlite3.Error as error:
        print("Failed to create database", error)
    finally:
        print("complete")

def db_insert_population_levels():
    try:
        cur = get_db()

        population_levels_csv = pd.read_csv('data/factbook-2015-table1-en.csv',
                                            engine='python', encoding="UTF-8",
                                            header=0, delimiter=";", skiprows=3,
                                            skipfooter=1, index_col=0)

        df_drop_last_2_rows = population_levels_csv.iloc[:-1]
        df_drop_last_2_rows.columns.values[0] = "Country"
        df_drop_last_2_rows.to_sql('population_levels', cur, if_exists='append', index=False)
        cur.close()
    except sqlite3.Error as error:
        print("Failed to insert", error)
    finally:
        print("complete")


@app.route('/population-levels', methods=['GET'])
def get_population_levels():
    """ A endpoint to retreive population levels data per country.
    ---
    get:
      description: Get all population level data.
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: Return a collection of countries and their figures per year.
          content:
            application/json:
              schema: PopulationLevelsSchema
    """
    try:
        cur = get_db().cursor()
        table_name = 'population_levels'
        result = cur.execute("""SELECT * FROM population_levels""").fetchall()
        cur.close()

        endpoint_obj = {}
        count = 0
        for country in result:
            count += 1
            endpoint_obj[country[1].lower().replace(" ", "-")] = {
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
        if cur:
            cur.close()
            print("closing db")


def db_real_household_disposable_income():
    print("creating the database")
    try:
        cur = get_db().cursor()

        SQL = '''CREATE TABLE IF NOT EXISTS real_household_disposable_income (CountryID INTEGER,
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
        cur.close()
    except sqlite3.Error as error:
        print("Failed to create database", error)
    finally:
        if cur:
            cur.close()
            print("closing db")

def db_insert_real_household_disposable_income():
    try:
        cur = get_db()

        real_household_disposable_income_csv = pd.read_csv('data/real-household-disposable-income.csv',
                                            engine='python', encoding="UTF-8",
                                            header=0, delimiter=";", skiprows=3,
                                            skipfooter=1, index_col=0)

        df_drop_last_2_rows = real_household_disposable_income_csv.iloc[:-1]
        df_drop_last_2_rows.columns.values[0] = "Country"
        df_drop_last_2_rows.to_sql('real_household_disposable_income', cur, if_exists='append', index=False)
        cur.close()
    except sqlite3.Error as error:
        print("Failed to insert", error)
    finally:
        print("complete")

@app.route('/real-household-disposable-income', methods=['GET'])
def get_real_household_disposable_income():
    try:
        cur = get_db().cursor()
        table_name = 'real_household_disposable_income'
        result = cur.execute("""SELECT * FROM real_household_disposable_income""").fetchall()
        cur.close()

        endpoint_obj = {}
        count = 0
        for country in result:
            count += 1
            endpoint_obj[country[1].lower().replace(" ", "-")] = {
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
        print("Not Working", error)
    finally:
        if cur:
            cur.close()
            print("closing db")

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


@app.route('/', methods=['GET'])
def get():
    db_real_household_disposable_income()
    db_insert_real_household_disposable_income()
    return jsonify({'message': 'World Hello'})


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
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True, threaded=True, port=5000)
