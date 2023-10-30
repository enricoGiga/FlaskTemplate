import os
from datetime import datetime
from datetime import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, g
from flask_caching import Cache
from flask_smorest import Api
from psycopg2 import pool

scheduler = BackgroundScheduler()

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
    app = Flask(__name__)

    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"

    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300

    # scheduler.add_job(check_event_statuses, 'interval', seconds=5)
    # scheduler.start()
    # Adding Flask-Caching configurations
    cache = Cache(app)
    cache.init_app(app)
    app.config["CACHE"] = cache  # Store the cache object in the server context

    @app.before_request
    def before_request():
        g.db = db_pool.getconn()

    @app.teardown_request
    def teardown_request(exception):
        db = g.pop('db', None)
        if db is not None:
            db_pool.putconn(db)

    api = Api(app)
    from server.resources.event import eventBlueprint
    from server.resources.search import searchBlueprint
    from server.resources.selection import selectionBlueprint
    from server.resources.sport import sportBlueprint
    api.register_blueprint(sportBlueprint)
    api.register_blueprint(eventBlueprint)
    api.register_blueprint(selectionBlueprint)
    api.register_blueprint(searchBlueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

