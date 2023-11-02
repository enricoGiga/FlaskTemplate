import functools

import psycopg2
from flask_smorest import abort


def create_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except psycopg2.IntegrityError as e:

            abort(http_status_code=409, message=e.pgerror)

    return wrapper
