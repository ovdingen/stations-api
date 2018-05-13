import argparse
import xmltodict
import sqlite3
import json
import requests
from requests.auth import HTTPBasicAuth

parser = argparse.ArgumentParser(description="importeert stationsxml naar sqlite")
parser.add_argument("-d", "--db", dest="db", help="sqlite databaselocatie", default="data/db.sqlite")
parser.add_argument("-c", "--credentials", dest="credentials", help="location of credentials", default="ns-credentials.json")


args = parser.parse_args()
with open(args.credentials) as data_file:    
    credentials = json.load(data_file)

r = requests.get('https://webservices.ns.nl/ns-api-stations-v2', auth=(credentials['user'], credentials['pass']))

xml = r.text 

stations = xmltodict.parse(xml)

#print(json.dumps(stations))
vals = []

for station in stations['Stations']['Station']:
    synonyms = [None, None, None, None]
    synonym_i = 0
    
    if station['Synoniemen'] is not None:
        if type(station['Synoniemen']['Synoniem']) is list:
            for synonym in station['Synoniemen']['Synoniem']:
                synonyms[synonym_i] = synonym
                synonym_i += 1
        else:
            synonyms[0] = station['Synoniemen']['Synoniem']

    cur_val = (station['Code'], station['Type'], station['Namen']['Kort'], station['Namen']['Middel'], station['Namen']['Lang'], station['Land'], station['UICCode'], station['Lat'], station['Lon'], synonyms[0], synonyms[1], synonyms[2], synonyms[3]) 
    vals.append(cur_val)

conn = sqlite3.connect(args.db)

c = conn.cursor()

c.executemany("REPLACE INTO stations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", vals)

conn.commit()
conn.close()
print(str(len(vals)) + " rows inserted")

#print(pp.pprint(xmltodict.parse(xml)))

