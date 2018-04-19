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
        self.assertTrue(isinstance(test1['businesses'], list))
        self.assertTrue(isinstance(test2['businesses'], list))
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
        self.assertTrue(type(result_list) == list)
        self.assertTrue(len(result_list) > 100)

        conn.close()

class TestProcessingComponents(unittest.TestCase):
    def test_map_graph(self):
        final_results = process_command(['chicago'])
        self.assertTrue(type(final_results), list)
        for item in final_results:
            self.assertEqual(item[0], 'Chicago')

    def test_price_graph(self):
        final_results = process_command(['new', 'york'])
        self.assertTrue(type(final_results), list)
        for item in final_results:
            self.assertEqual(item[0], 'New York')



if __name__ == '__main__':
    unittest.main()
