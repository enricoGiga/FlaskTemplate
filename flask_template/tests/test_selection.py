import unittest
from unittest.mock import patch

from app import create_app


class TestSelection(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('app.db_pool')
    def test_put(self, db_pool):
        mock_cursor = db_pool.getconn.return_value.cursor.return_value
        mocked_query_string = {'name': 'X',
                               'event': 'Basketball Match 1'
                               }
        body = {
            "price": "3.0",
            "active": False
        }

        expected_response = {
            "active": False,
            "event": "Basketball Match 1",
            "name": "X",
            "outcome": "Unsettled",
            "price": "3.00"
        }
        mock_cursor.fetchone.return_value = expected_response
        mock_cursor.fetchone.side_effect = [
            {'name': 'X', 'event': 'Basketball Match 1', 'price': '3.00',
             'active': False, 'outcome': 'Unsettled'},
            {'inactive_count': 1, 'total_count': 3},
            expected_response]

        response = self.client.put('/selection',
                                   query_string=mocked_query_string, json=body)
        self.assertEqual(mock_cursor.execute.call_count, 5)
        self.assertEqual(response.get_json(), expected_response)


if __name__ == '__main__':
    unittest.main()
