from flask import request, jsonify
from flask_smorest import Blueprint
from psycopg2.extras import RealDictCursor

from database import get_db

searchBlueprint = Blueprint("Search", "search", description="Operations on search")


# Helper function to execute SQL queries
def execute_query(query, args=()):
    db = get_db()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, args)
    results = cursor.fetchall()
    db.commit()
    cursor.close()
    return results


@searchBlueprint.route('/search', methods=['GET'])
def get():
    filters = request.args.to_dict()
    results = []
    # Construct the query based on the provided filters
    query = """
            SELECT distinct e.slug, e.scheduled_start, e.status, se.outcome
            FROM sport s
            LEFT JOIN event e ON s.name = e.sport
            LEFT JOIN selection se ON e.name = se.event
            WHERE  1=1 
        """
    args = []
    for key, value in filters.items():
        if key.startswith("event_"):
            column = "e." + key.replace("event_", "")
            query += f"AND {column}=%s "
            args.append((value,))

        elif key.startswith("sport_"):
            column = "s." + key.replace("sport_", "")
            query += f"AND {column}=%s "
            args.append((value,))

        elif key.startswith("selection_"):
            column = "se." + key.replace("selection_", "")
            query += f"AND {column}=%s "
            args.append((value,))

    results = execute_query(query=query, args=args)

    return jsonify(results)
