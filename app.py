import pandas as pd
import datetime as dt
import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hawaii.sqlite"
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
            Welcome to the home page! Below are all the available routes.

            http://127.0.0.1:5000/api/v1.0/precipitation
            Returns a JSON of date, station, and precipitation values.

            http://127.0.0.1:5000/api/v1.0/stations
            Returns a JSON list of stations from the dataset.

            http://127.0.0.1:5000/api/v1.0/tobs
            Returns a JSON list of date, station, and temperature observations for the previous year.

            http://127.0.0.1:5000/api/v1.0/search
            Pass a start date or both start and end dates. Returns JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
            """

    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})


@app.route("/api/v1.0/precipitation")
def prcp():
    try:
        prcp = Measurement.query.with_entities(Measurement.date, Measurement.station, Measurement.prcp).all()
        return jsonify(prcp)

    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})


@app.route("/api/v1.0/stations")
def stations():
    try:
        stations = Station.query.with_entities(Station.station).all()
        return jsonify(stations)

    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})


@app.route("/api/v1.0/tobs")
def tobs():
    date_last = Measurement.query.order_by(Measurement.id.desc()).first().date
    date_one_yr_ago = date_last - dt.timedelta(days=365)

    last_yr_tobs = Measurement.query.filter(Measurement.date >= date_one_yr_ago).with_entities(Measurement.date, Measurement.station, Measurement.tobs).all()
    
    try:
        return jsonify(last_yr_tobs)

    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})


@app.route("/api/v1.0/search")
def search():

    request_start = request.args.get("start")
    request_end = request.args.get("end")

    try:
        base_cmd = Measurement.query

        if request_start:
            base_cmd = base_cmd.filter(
                Measurement.date >= (dt.datetime.strptime(request_start, "%Y-%m-%d") - dt.timedelta(days=1))
            )

        if request_end:
            base_cmd = base_cmd.filter(
                Measurement.date <= dt.datetime.strptime(request_end, "%Y-%m-%d")
            )

        temps = base_cmd.with_entities(db.func.min(Measurement.tobs), db.func.avg(Measurement.tobs), db.func.max(Measurement.tobs)).all()
        keys = ["min", "mean", "max"]

        return jsonify({keys[i]:temps[0][i] for i in range(len(keys))})
        
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
