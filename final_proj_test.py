from final_proj import *
import unittest


class TestAPIS(unittest.TestCase):
    def get_data_from_yelp(term, location, limit):
        self.assertEqual(get_data_from_yelp('restaurant', 'Chicago'))
        self.assertIn(get_data_from_yelp('restaurant', 'Los Angeles'), 'Sugarfish')


    def get_WalkScore(latitude, longitude, address):
        self.assertEqual(get_WalkScore('', '', ''))


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



# class TestProcessing(unittest.TestCase):
#     def test_walksore()
#         self.assertEqual()
#         self.assertEqual()
#         self.assertEqual()
#         self.assertEqual()
#         self.assertEqual()





unittest.main()
