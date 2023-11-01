"""
App module for the REST API.
"""

import os

# from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, g
from flask_caching import Cache
from flask_smorest import Api
from psycopg2 import pool

# scheduler = BackgroundScheduler()

db_pool = pool.SimpleConnectionPool(
    1,  # minimum number of connections
    10,  # maximum number of connections
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    host=os.environ.get("DB_HOST"),
    port=5432,
)


# @handle_database_connection
# def check_event_statuses(cursor):
#     with server.app_context():
#         current_time = datetime.now()
#         # Convert the local time to UTC
#         utc_time = current_time.astimezone(timezone.utc)
#         query = """
#         SELECT * FROM event
#         WHERE scheduled_start <= %s AND status = 'Pending'
#         """
#         cursor.execute(query, (utc_time,))
#         events = cursor.fetchall()  # Implement a function to fetch all events from the database
#         for event in events:
#             current_time = datetime.now()
#             # Convert the local time to UTC
#             utc_time = current_time.astimezone(timezone.utc)
#
#             update_query = """
#                 UPDATE event SET status = %s, actual_start = %s WHERE name = %s
#             """
#             cursor.execute(update_query, ("Started", utc_time, event["name"]))


def create_app():
    """
    Create the Flask app and configure it.
    """
    flask_app = Flask(__name__)

    flask_app.config["API_TITLE"] = "Stores REST API"
    flask_app.config["API_VERSION"] = "v1"
    flask_app.config["OPENAPI_VERSION"] = "3.0.3"
    flask_app.config["OPENAPI_URL_PREFIX"] = "/"
    flask_app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"

    flask_app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    flask_app.config["PROPAGATE_EXCEPTIONS"] = True
    flask_app.config["CACHE_TYPE"] = "SimpleCache"
    flask_app.config["CACHE_DEFAULT_TIMEOUT"] = 300

    # scheduler.add_job(check_event_statuses, 'interval', seconds=5)
    # scheduler.start()
    # Adding Flask-Caching configurations
    cache = Cache(flask_app)
    cache.init_app(flask_app)
    flask_app.config["CACHE"] = cache  # Store the cache object in the server context

    @flask_app.before_request
    def before_request():
        g.db = db_pool.getconn()

    @flask_app.teardown_request
    def teardown_request(exception):
        db = g.pop('db', None)
        if db is not None:
            db_pool.putconn(db)
        if exception:
            print(f"An exception occurred: {exception}")

    api = Api(flask_app)
    from server.resources.event import eventBlueprint
    from server.resources.search import searchBlueprint
    from server.resources.selection import selectionBlueprint
    from server.resources.sport import sportBlueprint
    api.register_blueprint(sportBlueprint)
    api.register_blueprint(eventBlueprint)
    api.register_blueprint(selectionBlueprint)
    api.register_blueprint(searchBlueprint)

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
