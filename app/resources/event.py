from flask.views import MethodView
from flask_smorest import Blueprint
from psycopg2.extras import RealDictCursor

from database import get_db
from exceptions import create_exceptions
from schemas import EventSchema

eventBlueprint = Blueprint("Events", "events", description="Operations on events")


@eventBlueprint.route("/event")
class SportList(MethodView):
    @create_exceptions
    @eventBlueprint.arguments(EventSchema)
    @eventBlueprint.response(201, EventSchema)
    def post(self, event_data):
        with get_db() as db:
            cursor = db.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "INSERT INTO event (name, slug, active, type, sport, status, scheduled_start) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) "
                "RETURNING name, slug, active, type, sport, status, scheduled_start;",
                (event_data["name"], event_data["slug"], event_data["active"], event_data["type"],
                 event_data["sport"], event_data["status"], event_data["scheduled_start"]),
            )

            event = cursor.fetchone()
            db.commit()
            cursor.close()

        return event
