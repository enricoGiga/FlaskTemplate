from datetime import datetime
from datetime import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, g
from flask_caching import Cache
from flask_smorest import Api
from psycopg2.extras import RealDictCursor

from utility.database import SQLHelper

# Initialize the scheduler
scheduler = BackgroundScheduler()

@SQLHelper.handle_database_connection
def get_events(cursor):
    current_time = datetime.now()
    # Convert the local time to UTC
    utc_time = current_time.astimezone(timezone.utc)
    query = """
    SELECT * FROM event
    WHERE scheduled_start <= %s AND status = 'Pending'
    """
    cursor.execute(query, (utc_time,))
    events = cursor.fetchall()

    return events

@SQLHelper.handle_database_connection
def update_event_status(event_id, cursor):

    current_time = datetime.now()
    # Convert the local time to UTC
    utc_time = current_time.astimezone(timezone.utc)

    update_query = """
        UPDATE event SET status = %s, actual_start = %s WHERE name = %s
    """
    cursor.execute(update_query, ("Started", utc_time, event_id))


def check_event_statuses():
    with app.app_context():

        events = get_events()  # Implement a function to fetch all events from the database
        for event in events:
            update_event_status( event['name'])



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
    # Adding Flask-Caching configurations
    cache = Cache(app)
    cache.init_app(app)
    app.config["CACHE"] = cache  # Store the cache object in the app context

    # Create a function to close the database connection and return it to the pool
    @app.teardown_appcontext
    def close_db(error):
        if 'db' in g:
            g.db.commit()
            # Make sure any pending transactions are committed
            SQLHelper.get_connection_pool().putconn(g.db)
            g.pop('db', None)

    api = Api(app)
    from resources.event import eventBlueprint
    from resources.search import searchBlueprint
    from resources.selection import selectionBlueprint
    from resources.sport import sportBlueprint
    api.register_blueprint(sportBlueprint)
    api.register_blueprint(eventBlueprint)
    api.register_blueprint(selectionBlueprint)
    api.register_blueprint(searchBlueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    # Schedule the job to run periodically, for example every minute
    scheduler.add_job(check_event_statuses, 'interval', seconds=15)
    scheduler.start()
    app.run(host="0.0.0.0", port=5000)
