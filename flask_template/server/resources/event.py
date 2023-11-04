from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

from server.extensions.database import handle_database_connection
from server.schemas import EventSchema

eventBlueprint = Blueprint("Events", "events", description="Operations on events")


@eventBlueprint.route("/event")
class EventList(MethodView):
    @handle_database_connection
    @eventBlueprint.arguments(EventSchema)
    @eventBlueprint.response(201, EventSchema)
    def post(self, cursor, event_data):
        """Create a new event."""
        query = """\
        INSERT INTO event (name, slug, active, type, sport, status, scheduled_start) \
        VALUES (%s, %s, %s, %s, %s, %s, %s) \
        RETURNING name, slug, active, type, sport, status, scheduled_start;"""

        args = (
            event_data["name"], event_data["slug"], event_data["active"],
            event_data["type"],
            event_data["sport"], event_data["status"], event_data["scheduled_start"])
        cursor.execute(query, args)
        event = cursor.fetchone()

        return jsonify(event), 201
