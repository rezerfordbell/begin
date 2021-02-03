import unittest
import requests

BASE_API_URL = "https://randomuser.me/api/?format=json"


class TestMethods(unittest.TestCase):

    def test_api_works(self):
        result = requests.get(BASE_API_URL)
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()
