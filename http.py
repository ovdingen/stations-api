from flask import Flask, render_template, request
from math import sin, cos, sqrt, atan2, radians
import stations
import sqlite3
import operator
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return "OK"
@app.route("/nearest/")
def nearest():
    db = sqlite3.connect('data/db.sqlite')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    max_stations = request.args.get('max_entries')
    if max_stations is None:
        max_stations = 5
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return json.dumps({"status": "NOK", "error": "value_coord"})

    try:
        max_stations = int(max_stations)
    except ValueError:
        return json.dumps({"status": "NOK", "error": "value_max"})
    
    return json.dumps(stations.nearest_stations(db, lat, lon, max_stations))


@app.route("/station/<station>/")
def getstation(station):
    db = sqlite3.connect('data/db.sqlite')
    station = stations.get_station(db, station)
    if station is False:
        return json.dumps({"status": "NOK", "error": "NOT_FOUND"})
    
    return json.dumps({"status": "OK", "station": station})
