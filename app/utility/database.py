import os
from functools import wraps

from flask import g, jsonify
from psycopg2 import pool
from psycopg2.extras import RealDictCursor


class SQLHelper:

    @staticmethod
    def get_connection_pool():
        return pool.SimpleConnectionPool(
            1,  # minimum number of connections
            10,  # maximum number of connections
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            host=os.environ.get("DB_HOST"),
            port=5432,
        )

    @staticmethod
    def get_db():
        if 'db' not in g:
            g.db = SQLHelper.get_connection_pool().getconn()
        return g.db

    @staticmethod
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
            connection = None
            try:
                connection = SQLHelper.get_connection_pool().getconn()
                cursor = connection.cursor(cursor_factory=RealDictCursor)
                if is_method:
                    result = func(self, cursor, *args, **kwargs)
                else:
                    result = func(cursor, *args, **kwargs)
                connection.commit()
                return result
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            finally:
                if cursor:
                    cursor.close()

        return wrapper
