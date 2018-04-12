import requests
import json
import sys
import plotly
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
from requests_oauthlib import OAuth1
import secrets as secrets
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


CACHE_FNAME = 'final_project_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def params_unique_combination(url, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return url + "_".join(res)

def save_cache():
    full_text = json.dumps(CACHE_DICTION)
    cache_file_ref = open(CACHE_FNAME, 'w')
    cache_file_ref.write(full_text)
    cache_file_ref.close()

def load_cache():
    global CACHE_DICTION
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}

def make_request_using_cache(url, headers, params, verify=False):
    unique_ident = params_unique_combination(url, params)

    if unique_ident in CACHE_DICTION:
        print('Getting cached data...')
        return CACHE_DICTION[unique_ident]

    else:
        print('Making request for new data...')
        resp = requests.get('GET', url, headers=headers, params=params)
        CACHE_DICTION[unique_ident] = resp.text
        save_cache()
        return CACHE_DICTION[unique_ident]

def get_data_from_yelp(term, location, limit=50):
    url = 'https://api.yelp.com/v3/businesses/search'
    API_KEY = secrets.YELP_API_KEY
    headers = {
        'Authorization': 'Bearer {}'.format(API_KEY)
    }
    params = {'term': term, 'location': location, 'limit':50}
    uniq = params_unique_combination(url, params)
    if uniq in CACHE_DICTION:
        text = CACHE_DICTION[uniq]
        return text
    else:
        response = requests.get(url, headers=headers, params=params, verify=False)
        yelpinfo = json.loads(response.text)
        CACHE_DICTION[uniq] = yelpinfo
        save_cache()
        return yelpinfo
load_cache()
# get_data_from_yelp('restaurants', 'Wilmette')


def get_WalkScore(latitude, longitude, address):
    url = 'http://api.walkscore.com/score?format=json'
    apiKey = secrets.WALKABILITY_API_KEY
    params = {'lat': latitude, 'lon': longitude, 'address': address, 'wsapikey':apiKey}
    response = requests.get(url, params=params)
    uniq = params_unique_combination(url, params)
    if uniq in CACHE_DICTION:
        text = CACHE_DICTION[uniq]
        return text
    else:
        response = requests.get(url, params=params, verify=False)
        walkinfo = json.loads(response.text)
        CACHE_DICTION[uniq] = walkinfo
        save_cache()
        return walkinfo
load_cache()
# get_WalkScore(41.8846460590586, -87.6484126982138, '820 W Randolph St, Chicago IL')


DBNAME = 'final.db'
YELPWALKJSON = 'final_project_cache.json'

conn = sqlite3.connect(DBNAME)
cur = conn.cursor()
statement = 'DROP TABLE IF EXISTS "CITIES"'
cur.execute(statement)
conn.commit()
statement = 'DROP TABLE IF EXISTS "RESTAURANTS"'
cur.execute(statement)
conn.commit()
statement = 'DROP TABLE IF EXISTS "WALKSCORE"'
cur.execute(statement)
conn.commit()

statement = '''
CREATE TABLE IF NOT EXISTS 'CITIES' (
‘id’ INTEGER PRIMARY KEY,
‘name’ TEXT,
‘display_address’ TEXT,
‘latitude’ REAL,
‘longitude’ REAL
)
'''
cur.execute(statement)
conn.commit()

statement = '''
CREATE TABLE IF NOT EXISTS 'RESTAURANTS' (
'id' INTEGER PRIMARY KEY,
'rating' DECIMAL,
‘review_count’ INTEGER,
'categories' TEXT,
'title' TEXT,
'price' TEXT,
'city' TEXT
)
'''
cur.execute(statement)
conn.commit()


statement = '''
CREATE TABLE IF NOT EXISTS 'WALKSCORE' (
'walkscore' INTEGER,
'snapped_lat' INTEGER,
'snapped_lon' INTEGER,
'address' TEXT
)
'''
cur.execute(statement)
conn.commit()


json_file = open('final_project_cache.json', 'r')
read_j = json_file.read()
list_file = json.loads(read_j)


for info in list_file.values():
    name = info["businesses"][1]["name"]
    display_address = info["businesses"][1]["name"]
    latitude = info["latitude"]
    longitude = info["businesses"][1]["name"]

    insertion = (None, name, display_address, latitude, longitude)
    statement = '''
    INSERT INTO 'CITIES'
    Values (?, ?, ?, ?, ?)
    '''
    cur.execute(statement, insertion)
conn.commit()

# for info in list_file.values():
#     rating = info
#     review_count = info
#     categories = info
#     title = info
#     price = info
#     city = info
#
#     statement = '''
#     INSERT INTO 'RESTAURANTS'
#     Values (?, ?, ?, ?, ?, ?, ?)
#     '''
#     cur.execute(statement, insertion)
# conn.commit()
#
#
# for info in list_file.values():
#     walkscore = info
#     snapped_lat = info
#     snapped_lon = info
#     address = info
#     statement = '''
#     INSERT INTO 'WALKSCORE'
#     Values (?, ?, ?, ?, ?)
#     '''
#     cur.execute(statement, insertion)
# conn.commit()
#
#
#
#


#--------------------------------------------------------------------------------------------------------

# if __name__ == '__main__':
#     main()
