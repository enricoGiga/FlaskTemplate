import unittest
from datetime import datetime, timezone


class MyTestCase(unittest.TestCase):
    def test_something(self):
        query = """
            SELECT distinct e.slug, e.scheduled_start, e.status
            FROM sport s
            JOIN event e ON s.name = e.sport
            JOIN selection se ON e.name = se.event
            WHERE  1=1 
        """
        args = []
        filters = {'event_status': 'Pending', 'sport_name': 'Football'}
        for key, value in filters.items():
            if key.startswith("event_"):
                column = "e." + key.replace("event_", "")
                query += f"AND {column}=%s "
                args.append((value,))

            if key.startswith("sport_"):
                column = "s." + key.replace("sport_", "")
                query += f"AND {column}=%s "
                args.append((value,))


            if key.startswith("selection_"):
                column = "se." + key.replace("selection_", "")
                query += f"AND {column}=%s "
                args.append((value,))

if __name__ == '__main__':
    unittest.main()
