import sqlite3
from math import sin, cos, sqrt, atan2, radians
import operator

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def get_stations(conn):
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = c.execute("SELECT * FROM stations")
    returndata = []
    for row in rows:
        returndata.append(dict_from_row(row))
    return returndata

def get_station(conn, code):
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    params = (code.upper(),)
    rows = c.execute("SELECT * FROM stations WHERE code = ? LIMIT 1", params)
    returndata = False
    for row in rows:
        returndata = dict_from_row(row)
    
    return returndata

def nearest_stations(conn, lat, lon, max_entries):
    sd = get_stations(conn)
    lat1 = radians(lat)
    lon1 = radians(lon)
    # approximate radius of earth in km
    R = 6373.0

    for station in sd:
        lat2 = radians(station['lat'])
        lon2 = radians(station['lon'])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        station['distance'] = distance

    sd.sort(key=operator.itemgetter('distance'))

    returndata = {"status": "OK", "stations": sd[:max_entries]}

    return returndata