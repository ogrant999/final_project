import unittest, sqlite3
from final_proj import *
import requests
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

conn = sqlite3.connect('final.db')
cur = conn.cursor()

# You must write unit tests to show that the data access, storage, and
# processing components of your project are working correctly.
# that your database is correctly constructed and can satisfy queries that are necessary
# for your program, and that your data
# processing produces the results and data structures you need for presentation.

class Test_API(unittest.TestCase):
    def test_get_data_from_yelp(self):
        test1 = get_data_from_yelp('restaurants', 'Ann Arbor', 10)
        test2 = get_data_from_yelp('restaurants', 'Los Angeles', 10)
        self.assertEqual((test1['businesses'][0]["name"]), 'Poke Fish')
        self.assertEqual((test2['businesses'][0]["display_phone"]), "(310) 362-6115")
        self.assertTrue(type(test1) == dict)
        self.assertTrue(type(test2) == dict)

    def test_get_WalkScore(self):
        test1 = get_WalkScore('40.7263139141197', '-73.9864901976935', '95 1st Ave New York, NY')
        self.assertEqual(test1[0:52], "http://api.walkscore.com/score?format=jsonaddress-95")

class TestDatabase(unittest.TestCase):
    def test_bar_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT name FROM RESTAURANTS'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Girl & the Goat'), result_list[0])
        self.assertEqual(len(result_list), 200)
        self.assertTrue(type(result_list) == list)

    def test_walk_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT walkscore FROM WALK'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(((97,)), result_list[0])
        self.assertEqual(len(result_list), 200)
        self.assertTrue(type(result_list) == list)

    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT city, name, rating, walkscore, title, price, review_count, lat, lon  ' \
        'FROM RESTAURANTS r ' \
        'JOIN WALK w on r.walk_id = w.id '
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(((('Miami', 'The Taco Stand', 4.5, 95, 'Mexican', '$$', 53, 25.80088, -80.20138))), result_list[150])
        self.assertEqual((('Detroit', 'Wright & Company', 4, 99, 'Gastropubs', '$$', 696, 42.3352279663086, -83.0490188598633)), result_list[23])
        self.assertTrue(type(result_list) == list)

        conn.close()

class TestProcessingComponents(unittest.TestCase):
    def test_map_graph(self):
        final_results = process_command('type chicago')
        results = map_graph(final_results)
        self.assertEqual(results, True)
        # self.assertEqual(results[0][3], 97)

    # def test_price_graph(self):
    #     data_in = process_command('price orlando')
    #     results = map_price_graph(data_in)
    #     self.assertEqual(results[0][3], 4.5)
    #     self.assertEqual(results[2][1], 'Pio Pio')



if __name__ == '__main__':
    unittest.main()
