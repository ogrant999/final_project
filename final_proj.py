import requests
import json
import sys
import plotly
import requests
import numpy as np
import pandas as pd
import sqlite3
from requests_oauthlib import OAuth1
import secrets as secrets
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


CACHE_FNAME = 'final_project_cache.json'
WALK_CACHE_FNAME = 'final_project_walk_cache.json'
DBNAME = 'final.db'
CACHE_DICTION = {}
CACHE_DICTION2 = {}

REFRESH_YELP = True
REFRESH_WALKS = False

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

def save_cache():
    full_text = json.dumps(CACHE_DICTION2)
    cache_file_ref = open(WALK_CACHE_FNAME, 'w')
    cache_file_ref.write(full_text)
    cache_file_ref.close()

def load_cache():
    global CACHE_DICTION2
    try:
        cache_file = open(WALK_CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION2 = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION2 = {}

def make_request_using_cache2(url, headers, params, verify=False):
    unique_ident = params_unique_combination(url, params)

    if unique_ident in CACHE_DICTION2:
        print('Getting cached data...')
        return CACHE_DICTION2[unique_ident]

    else:
        print('Making request for new data...')
        resp = requests.get('GET', url, headers=headers, params=params)
        CACHE_DICTION2[unique_ident] = resp.text
        save_cache()
        return CACHE_DICTION2[unique_ident]


def get_data_from_yelp(term, location, limit=50):
    url = 'https://api.yelp.com/v3/businesses/search'
    API_KEY = secrets.YELP_API_KEY
    headers = {
        'Authorization': 'Bearer {}'.format(API_KEY)
    }
    params = {'term': term, 'location': location, 'limit': limit}
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
# get_data_from_yelp('restaurants', 'New York')

def get_WalkScore(latitude, longitude, address):
    url = 'http://api.walkscore.com/score?format=json'
    apiKey = secrets.WALKABILITY_API_KEY
    params = {'lat': latitude, 'lon': longitude, 'address': address, 'wsapikey':apiKey}
    response = requests.get(url, params=params)
    uniq = params_unique_combination(url, params)
    if uniq in CACHE_DICTION2:
        text = CACHE_DICTION2[uniq]
        return text
    else:
        response = requests.get(url, params=params, verify=False)
        walkinfo = json.loads(response.text)
        CACHE_DICTION2[uniq] = walkinfo
        save_cache()
        return walkinfo


def main():
    global CACHE_FNAME, DBNAME, CACHE_DICTION, REFRESH_YELP, REFRESH_WALKS

    #load_cache()
    # delete/ignore final_project_cache.json
    if REFRESH_YELP == True:
        get_data_from_yelp('restaurants', 'Chicago', limit=25)
        get_data_from_yelp('restaurants', 'Detroit', limit=25)
    else:
        load_cache()

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
    CREATE TABLE IF NOT EXISTS 'RESTAURANTS' (
    'name' TEXT,
    'id' TEXT,
    'rating' DECIMAL,
    ‘review_count’ INTEGER,
    'title' TEXT,
    'price' TEXT,
    ‘latitude’ DECIMAL,
    ‘longitude’ DECIMAL,
    'city' TEXT,
    'display_address' TEXT
    )
    '''
    cur.execute(statement)
    conn.commit()


    statement = '''
    CREATE TABLE IF NOT EXISTS 'CITIES' (
    ‘id’ TEXT,
    'name' TEXT,
    'lat' DECIMAL,
    'lon' DECIMAL,
    'city' TEXT
    )
    '''
    cur.execute(statement)
    conn.commit()


    statement = '''
    CREATE TABLE IF NOT EXISTS 'WALKSCORE' (
    'id' INTEGER PRIMARY KEY,
    'walkscore' INTEGER,
    'snapped_lat' INTEGER,
    'snapped_lon' INTEGER
    )
    '''
    cur.execute(statement)
    conn.commit()



    for key in CACHE_DICTION.keys():
        city_rst = CACHE_DICTION[key]
        for city_key in city_rst:
            business_list = city_rst['businesses']
        for business in business_list:
            b_id = business['id']
            b_name = business['name']
            b_categories = business['categories']
            try:
                b_price = business['price']
            except:
                b_price = "None"
            b_reviewcount = business['review_count']
            b_rating = business['rating']
            b_categories = business['categories']
            b_title = b_categories[0]['title']
            b_coords = business['coordinates']
            b_lat = b_coords['latitude']
            b_lon = b_coords['longitude']
            b_loc = business['location']
            b_city = b_loc['city']
            b_disp_addr = b_loc['display_address'][0]
            b_disp_addr2 = b_loc['display_address'][1]
            b_display_addr = str(b_disp_addr + " " + b_disp_addr2)
            statement = '''INSERT INTO 'RESTAURANTS' Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            insertion = (b_name, b_id, b_rating, b_reviewcount, b_title, b_price, b_lat, b_lon, b_city, b_display_addr)
            cur.execute(statement, insertion)
            conn.commit()
            if REFRESH_WALKS == True:
                get_WalkScore(b_lat, b_lon, " ".join(b_disp_addr))

    # get_WalkScore('40.6935414945595', '-73.9858423383398', '2 MetroTech Ctr Metrotech Campus Brooklyn, NY 11201')
    for key in CACHE_DICTION.keys():
        city_rst = CACHE_DICTION[key]
        for city_key in city_rst:
            business_list = city_rst['businesses']
        for business in business_list:
            b_id = business['id']
            b_name = business['name']
            b_lat = b_coords['latitude']
            b_lon = b_coords['longitude']
            b_loc = business['location']
            b_city = b_loc['city']
            statement = '''INSERT INTO 'CITIES' Values (?, ?, ?, ?, ?)'''
            insertion = (b_id, b_name, b_lat, b_lon, b_city)
            cur.execute(statement, insertion)
            conn.commit()
        for key in CACHE_DICTION2.keys():
            walk = CACHE_DICTION2[key]
            # print(walk)
            for score in walk:
                walkscore = walk['walkscore']
                lat = walk['snapped_lat']
                lon = walk['snapped_lon']
                statement = '''INSERT INTO 'WALKSCORE' Values (?, ?, ?, ?)'''
                insertion = (None, walkscore, lat, lon)
                cur.execute(statement, insertion)
                conn.commit()


#data processing code



#data presentation code


#--------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
