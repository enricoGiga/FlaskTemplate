import unittest
from unittest.mock import patch
from datetime import datetime, timezone
from app import create_app


class TestSearchBlueprint(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('app.db_pool')
    def test_get_event_start_with(self, db_pool):
        mock_cursor = db_pool.getconn.return_value.cursor.return_value
        expected_result = [{'event_id': 1, 'event_name': 'Test Event'}]
        mock_cursor.fetchall.return_value = expected_result

        mock_cursor.execute.return_value = None

        mock_start_with = 'Mocked'

        response = self.client.get('/search/event_start_with',
                                   query_string={'start_with': mock_start_with})
        data = response.get_json()

        mock_cursor.execute.assert_called_once()
        self.assertEqual(data, expected_result)

    @patch('app.db_pool')
    def test_get_events_active_selections_count(self, db_pool):
        mock_cursor = db_pool.getconn.return_value.cursor.return_value
        expected_result = [
            {'name': 'Football Match 1', 'scheduled_start': '2023-10-20 15:00:00.000000'}]
        mock_cursor.fetchall.return_value = expected_result

        mock_threshold = 'threshold'

        response = self.client.get('/search/events_active_selections_count',
                                   query_string={'start_with': mock_threshold})

        data = response.get_json()

        mock_cursor.execute.assert_called_once()
        self.assertEqual(data, expected_result)

    @patch('app.db_pool')
    def test_get_events_scheduled_in_timeframe(self, db_pool):
        mock_cursor = db_pool.getconn.return_value.cursor.return_value

        time = datetime.now()
        utc_time = time.astimezone(timezone.utc)
        now = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        expected_result = [
            {
                "name": "Test Event",
                "slug": "tests-event",
                "active": True,
                "type": "type",
                "sport": "sport",
                "status": "status",
                "scheduled_start": now
            }]
        mock_cursor.fetchall.return_value = expected_result



        response = self.client.get('/search/events_active_selections_count',
                                   query_string={'start_time': 'mock_start_time',
                                                 'end_time': 'mock_end_time',
                                                 'timezone': 'mock_timezone'})

        data = response.get_json()

        mock_cursor.execute.assert_called_once()
        self.assertEqual(data, expected_result)

    # @patch('app.db_pool')
    # def test_get(self, db_pool):
    #     mock_request.args.to_dict.return_value = {
    #         "event_example_key": "example_value",
    #         "sport_example_key": "example_value",
    #         "selection_example_key": "example_value"
    #     }
    #     mock_cursor = MagicMock()
    #     expected_result = [
    #         (1, "example_event_1", "example_status", "example_outcome"),
    #         (2, "example_event_2", "example_status", "example_outcome")]
    #
    #     mock_cursor.fetchall.return_value = expected_result
    #
    #     result = searchBlueprint.get(mock_cursor)
    #
    #     self.assertEqual(result.json, expected_result)


if __name__ == '__main__':
    unittest.main()
