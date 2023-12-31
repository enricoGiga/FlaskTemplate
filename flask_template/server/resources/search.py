from flask import request, jsonify
from flask_smorest import Blueprint

from server.extensions.database import handle_database_connection

searchBlueprint = Blueprint("Search", "search", description="Operations on search")


@searchBlueprint.route('/search/event_start_with', methods=['GET'])
@handle_database_connection
def get_event_start_with(cursor):
    """
    Get events starting with a specific string.
    """

    start_with = request.args.get("start_with")
    query = """
            SELECT * FROM event
            WHERE name LIKE %s;
            """
    cursor.execute(query, (start_with + '%',))
    results = cursor.fetchall()
    return jsonify(results)


@searchBlueprint.route('/search/events_active_selections_count', methods=['GET'])
@handle_database_connection
def get_events_active_selections_count(cursor):
    """
    Get events with a minimum number of active selections greater than or equal to the provided threshold.
    """
    start_with = request.args.get("threshold")
    query = """
            SELECT e.name, e.scheduled_start
            FROM event e
            JOIN (
                SELECT event, COUNT(*) as active_selections_count
                FROM selection
                WHERE active = TRUE
                GROUP BY event
                HAVING COUNT(*) >= %s
            ) s ON e.name = s.event;

            """

    cursor.execute(query, start_with)
    results = cursor.fetchall()
    return jsonify(results)


@searchBlueprint.route('/search/events_scheduled_in_timeframe', methods=['GET'])
@handle_database_connection
def get_events_scheduled_in_timeframe(cursor):
    """
    Get events scheduled to start in a specific timeframe for a specific timezone.
    """
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    timezone = request.args.get("timezone")

    query = """
            SELECT * FROM event
            WHERE scheduled_start AT TIME ZONE 'UTC' AT TIME ZONE %s
            BETWEEN %s AND %s;
            """
    cursor.execute(query, (timezone, start_time, end_time))
    results = cursor.fetchall()
    return jsonify(results)


