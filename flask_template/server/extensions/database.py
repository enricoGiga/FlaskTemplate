from functools import wraps

from flask import g, jsonify
from psycopg2.extras import RealDictCursor


def handle_database_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        is_method = False
        if len(args) > 0 and hasattr(args[0], '__class__'):
            is_method = True
            self, *args = args
        else:
            self = None

        cursor = None
        try:
            database = g.db
            cursor = g.db.cursor(cursor_factory=RealDictCursor)
            if is_method:
                result = func(self, cursor, *args, **kwargs)
            else:
                result = func(cursor, *args, **kwargs)
            database.commit()
            return result
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if cursor:
                cursor.close()

    return wrapper
