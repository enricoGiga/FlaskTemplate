import os

import psycopg2
from flask import g


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            host=os.environ.get("DB_HOST"),
            port=5432,
        )
    return g.db
