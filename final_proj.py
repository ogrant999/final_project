import requests
import json
import sys
import plotly
import requests
import numpy as np
import pandas as pd
import sqlite3
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

#calling APIs

def get_data_from_yelp(term, location, limit=100):
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
        #get_data_from_yelp('restaurants', 'New York')

def get_WalkScore(latitude, longitude, address):
    url = 'http://api.walkscore.com/score?format=json'
    apiKey = secrets.WALKABILITY_API_KEY
    params = {'lat': latitude, 'lon': longitude, 'address': address, 'wsapikey':apiKey}
    response = requests.get(url, params=params)
    uniq = params_unique_combination(url, params)
    #print(uniq)
    if uniq in CACHE_DICTION2:
        text = CACHE_DICTION2[uniq]
    else:
        response = requests.get(url, params=params, verify=False)
        walkinfo = json.loads(response.text)
        #print(walkinfo)
        CACHE_DICTION2[uniq] = walkinfo
        save_cache()
    return uniq


def main():
    print("Start")
    global CACHE_FNAME, DBNAME, CACHE_DICTION, REFRESH_YELP, REFRESH_WALKS

    #load_cache()
    # delete/ignore final_project_cache.json
    if REFRESH_YELP == True:
        get_data_from_yelp('restaurants', 'Chicago', limit=10)
        get_data_from_yelp('restaurants', 'Detroit', limit=10)
        get_data_from_yelp('restaurants', 'Los Angeles', limit=10)
        get_data_from_yelp('restaurants', 'New York', limit=10)
        get_data_from_yelp('restaurants', 'Atlanta', limit=10)
        get_data_from_yelp('restaurants', 'San Francisco', limit=10)
        get_data_from_yelp('restaurants', 'Orlando', limit=10)
        get_data_from_yelp('restaurants', 'Miami', limit=10)
        get_data_from_yelp('restaurants', 'Philadelphia', limit=10)
        get_data_from_yelp('restaurants', 'St. Louis', limit=10)
    else:
        load_cache()

#create databases

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = 'DROP TABLE IF EXISTS "RESTAURANTS"'
    cur.execute(statement)
    conn.commit()
    statement = 'DROP TABLE IF EXISTS "WALK"'
    cur.execute(statement)
    conn.commit()


    statement = '''
    CREATE TABLE IF NOT EXISTS 'RESTAURANTS' (
    'name' TEXT,
    'id' TEXT,
    'rating' DECIMAL,
    'review_count' INTEGER,
    'title' TEXT,
    'price' TEXT,
    'lat' DECIMAL,
    'lon' DECIMAL,
    'city' TEXT,
    'display_address' TEXT,
    'walk_id' INTEGER
    )
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
    CREATE TABLE IF NOT EXISTS 'WALK' (
    'id' INTEGER,
    'walkscore' INTEGER
    )
    '''
    cur.execute(statement)
    conn.commit()

#populate databases
    walk_id = 1
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
            b_loc = business['location']
            b_disp_addr = b_loc['display_address'][0]
            b_disp_addr2 = b_loc['display_address'][1]
            b_display_addr = str(b_disp_addr + " " + b_disp_addr2)
            b_city = b_loc['city']
            b_title = b_categories[0]['title']
            b_coords = business['coordinates']
            b_lat = b_coords['latitude']
            b_lon = b_coords['longitude']

            key = get_WalkScore(b_lat, b_lon, b_display_addr)
            got_walk_id = False
            try:
                walkscore = CACHE_DICTION2[key]['walkscore']
                statement = '''INSERT INTO 'WALK' Values (?, ?)'''
                insertion = (walk_id, walkscore)
                cur.execute(statement, insertion)
                conn.commit()
                got_walk_id = True
            except KeyError:
                print(CACHE_DICTION2[key])
                pass

            walk_id_to_insert = walk_id if got_walk_id else None

            statement = '''INSERT INTO 'RESTAURANTS' Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            insertion = (b_name, b_id, b_rating, b_reviewcount, b_title, b_price, b_lat, b_lon, b_city, b_display_addr, walk_id_to_insert)
            cur.execute(statement, insertion)
            conn.commit()
            if got_walk_id:
                walk_id += 1

#--------------------------------------------------------------------------------------------------------
#data processing code

def process_command(command):
    cities = []
    for city in command:
        cities.append("'" + city.lower() + "'")
    print(cities)

    cities_string = ",".join(cities)

    statement = 'SELECT city, name, rating, walkscore, title, price, review_count  ' \
    'FROM RESTAURANTS r ' \
    'JOIN WALK w on r.walk_id = w.id ' \
    'WHERE lower(city) in (' + cities_string + ')'

    print(statement)

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    cur.execute(statement)
    results = cur.fetchall()
    return results

#--------------------------------------------------------------------------------------------------------
#data presentation code

def interactive_prompt():
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')
        wordslst = response.split()
        if response == 'exit':
            print("bye!")
        elif len(wordslst) == 0:
            print("Please enter a command.")
            continue
        command = wordslst[0]
        final_results = process_command(wordslst[1:])
        if len(final_results) == 0:
            print("No results for that query.")
        if command == "rating":
            print("Ratings")
            print(final_results)
        else:
            print("Command not recognized: {}".format(response))


#--------------------------------------------------------------------------------------------------------

if __name__=="__main__":
    #main()
    interactive_prompt()
