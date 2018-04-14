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

def main():
    global CACHE_FNAME, DBNAME, CACHE_DICTION, REFRESH_YELP, REFRESH_WALKS

    #load_cache()
    # delete/ignore final_project_cache.json
    if REFRESH_YELP == True:
        get_data_from_yelp('restaurants', 'Chicago', limit=5)
        get_data_from_yelp('restaurants', 'Detroit', limit=5)
    else:
        load_cache()

    for key in CACHE_DICTION.keys():
        print(key)
        city_rst = CACHE_DICTION[key]
        for city_key in city_rst:
            print("--" + str(city_key))
        business_list = city_rst['businesses']
        for business in business_list:
            print("----" + str(business))
            b_id = business['id']
            b_name = business['name']
            b_categories = business['categories']
            #b_price = business['price']
            b_coords = business['coordinates']
            b_lat = b_coords['latitude']
            b_lon = b_coords['longitude']
            b_loc = business['location']
            b_disp_addr = b_loc['display_address']
            print("ID: " + str(b_id))
            print("NAME: " + str(b_name))
            print("LAT: "+ str(b_lat))
            print("LON:" + str(b_lon))
            print("ADR: " + str(b_disp_addr))
            statement = ''' INSERT INTO RESTAURANTS (b_coords, b_lat, b_lon, b_loc, b_disp_addr) VALUES (?, ?, ?, ?, ?)'''
            if REFRESH_WALKS == True:
                get_WalkScore(b_lat, b_lon, " ".join(b_disp_addr))
    for key in WALK_CACHE_DICTION.keys():
        pass

    # conn = sqlite3.connect(DBNAME)
    # cur = conn.cursor()
    # statement = 'DROP TABLE IF EXISTS "CITIES"'
    # cur.execute(statement)
    # conn.commit()
    # statement = 'DROP TABLE IF EXISTS "RESTAURANTS"'
    # cur.execute(statement)
    # conn.commit()
    # statement = 'DROP TABLE IF EXISTS "WALKSCORE"'
    # cur.execute(statement)
    # conn.commit()
    #
    # statement = '''
    # CREATE TABLE IF NOT EXISTS 'CITIES' (
    # ‘id’ INTEGER PRIMARY KEY,
    # 'city' TEXT
    # )
    # '''
    # cur.execute(statement)
    # conn.commit()
    #
    # statement = '''
    # CREATE TABLE IF NOT EXISTS 'RESTAURANTS' (
    # 'id' INTEGER PRIMARY KEY,
    # 'rating' DECIMAL,
    # ‘review_count’ INTEGER,
    # 'categories' TEXT,
    # 'title' TEXT,
    # 'price' TEXT,
    # 'city_id' INTEGER,
    # ‘display_address’ TEXT,
    # ‘latitude’ REAL,
    # ‘longitude’ REAL
    # )
    # '''
    # cur.execute(statement)
    # conn.commit()
    #
    #
    # statement = '''
    # CREATE TABLE IF NOT EXISTS 'WALKSCORE' (
    # 'id' INTEGER PRIMARY KEY,
    # 'walkscore' INTEGER,
    # 'snapped_lat' INTEGER,
    # 'snapped_lon' INTEGER,
    # 'address' TEXT
    # )
    # '''
    # cur.execute(statement)
    # conn.commit()
    #
    #
    # json_file = open('final_project_cache.json', 'r')
    # read_j = json_file.read()
    # list_file = json.loads(read_j)
    # for key in list_file.keys():
    #     value = list_file[key]
    #     print( "\n" + str(key) + " = " + str(value) )



# for key,info in list_file.values():
#     name = info[[1]
#     display_address = info[2]
#     latitude = info["businesses"][1]["name"]
#     longitude = info["businesses"][1]["name"]
#
#     insertion = (None, name, display_address, latitude, longitude)
#     statement = '''
#     INSERT INTO 'CITIES'
#     Values (?, ?, ?, ?, ?)
#     '''
#     cur.execute(statement, insertion)
# conn.commit()

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



#data processing code



#data presentation code


#--------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
