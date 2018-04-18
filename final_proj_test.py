import unittest
from final_proj import *



class Test_APIS(unittest.TestCase):
    def get_data_from_yelp(term, location, limit):
        test1 = get_data_from_yelp('restaurant', 'Chicago')
        test2 = get_data_from_yelp('restaurant', 'Los Angeles')
        self.assertIn('test2', 'The Purple Pig')
        self.assertIn('test2', 'Sugarfish')


#     def get_WalkScore(latitude, longitude, address):
#         self.assertEqual(get_WalkScore('40.7263139141197', '-73.9864901976935', '95 1st Ave New York, NY'), "'http://api.walkscore.com/score?format=jsonaddress-95 1st Ave New York, NY 10003_lat-40.7263139141197_lon--73.9864901976935_wsapikey-823ebf192a9537ddb2cbb92ea29ff225': {"status": 1, "walkscore": 100, "description": "Walker's Paradise", "updated": "2017-10-31 21:30:18.580520", "logo_url": "https://cdn.walk.sc/images/api-logo.png", "more_info_icon": "https://cdn.walk.sc/images/api-more-info.gif", "more_info_link": "https://www.redfin.com/how-walk-score-works", "ws_link": "https://www.walkscore.com/score/95-1st-Ave-New-York-NY-10003/lat=40.7263139141197/lng=-73.9864901976935/?utm_source=umich.edu&utm_medium=ws_api&utm_campaign=ws_api", "help_link": "https://www.redfin.com/how-walk-score-works", "snapped_lat": 40.7265, "snapped_lon": -73.986}")
#
#
# class TestDatabase(unittest.TestCase):
#     def test_bar_table(self):
#         conn = sqlite3.connect(DBNAME)
#         cur = conn.cursor()
#
#         sql = 'SELECT name FROM RESTAURANTS'
#         results = cur.execute(sql)
#         result_list = results.fetchall()
#         self.assertIn(('WJ Noodles', result_list)
#         self.assertEqual(len(result_list), 100)
#
#     def test_walk_table(self):
#         conn = sqlite3.connect(DBNAME)
#         cur = conn.cursor()
#         sql = 'SELECT '
#         results =
#         result_list =
#         self.assertIn()
#         self.assertEqual()
#
#
#         conn.close()
#
# class TestProcessing(unittest.TestCase):
#     def test_walksore()
#         self.assertEqual()
#         self.assertEqual()
#         self.assertEqual()
#         self.assertEqual()
#         self.assertEqual()
#




unittest.main()
