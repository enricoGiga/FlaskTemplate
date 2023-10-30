import unittest
from datetime import datetime, timezone
from unittest.mock import patch, Mock

from app import create_app
from server.schemas import EventSchema


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('app.db_pool')
    def test_post(self, db_pool):
        mock_cursor = db_pool.getconn.return_value.cursor.return_value

        time = datetime.now()
        utc_time = time.astimezone(timezone.utc)
        now = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        expected_data = {
            "name": "Test Event",
            "slug": "tests-event",
            "active": True,
            "type": "type",
            "sport": "sport",
            "status": "status",
            "scheduled_start": now
        }
        # deserialization
        loaded_data = EventSchema().load(expected_data)
        # serialization
        serialized_data = EventSchema().dump(loaded_data)
        mock_cursor.fetchone = Mock(return_value=serialized_data)

        data = {
            "name": "Test Event",
            "slug": "tests-event",
            "active": True,
            "type": "type",
            "sport": "sport",
            "status": "status",
            "scheduled_start": "2023-10-22 12:00:00"
        }

        response = self.client.post('/event', json=data)
        mock_cursor.fetchone.assert_called_once()
        mock_cursor.execute.assert_called_once()
        self.assertEqual(response.status_code, 201)
        response_data = response.get_json()
        self.assertEqual(response_data, expected_data)



if __name__ == '__main__':
    unittest.main()
