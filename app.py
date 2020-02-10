# import numpy as np
import pandas as pd
import datetime as dt
import os

# # Python SQL toolkit and Object Relational Mapper
# import sqlalchemy
# from sqlalchemy import Column, Integer, String, Float, Date
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.path.join("Resources", "sqlite:///hawaii.sqlite")
db = SQLAlchemy(app)

class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(getattr(self, column.name), dt.datetime)
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }


class Measurement(db.Model, DictMixIn):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "measurement"
    id = db.Column(db.Integer(), primary_key=True)
    station = db.Column("station", db.String())
    date = db.Column("date", db.Date())
    prcp = db.Column("prcp", db.Float())
    tobs = db.Column("tobs", db.Integer())


class Station(db.Model, DictMixIn):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "station"
    id = db.Column(db.Integer(), primary_key=True)
    station = db.Column("station", db.String())
    name = db.Column("name", db.String())
    latitude = db.Column("latitude", db.Float())
    longitude = db.Column("longitude", db.Float())
    elevation = db.Column("elevation", db.Float())


@app.route("/")
def home():
    try:
        return """
            Welcome to the home page.

            Here are all the available routes.
            /api/v1.0/precipitation: Returns a JSON of date and precipitation values.
            /api/v1.0/stations: Returns a JSON list of stations from the dataset.
            /api/v1.0/tobs: Returns a JSON list of temperature observations for the previous year.
            /api/v1.0/search: Pass a start date or both start and end dates. Returns JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
            """
    
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})


@app.route("/api/v1.0/precipitation")
def prcp():
    try:
        return "Precipation API"
    
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})


@app.route("/api/v1.0/stations")
def stations():
    try:
        return "Stations API"
    
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})


@app.route("/api/v1.0/tobs")
def tobs():
    try:
        return "TOBS API"
    
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})


@app.route("/api/v1.0/search")
def search():

    request_start = request.args.get("start")
    request_end = request.args.get("end")
    
    try:
        base_cmd = Measurement.query

        if request_start:
            base_cmd = base_cmd.filter(Measurement.date >= dt.datetime.strptime(request_start, "%Y-%m-%d"))
        
        if request_end:
            base_cmd = base_cmd.filter(Measurement.date <= dt.datetime.strptime(request_end, "%Y-%m-%d"))

        data = base_cmd.all()

        return "Search API" # jsonify([measurement.to_dict() for measurement in data])

    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
