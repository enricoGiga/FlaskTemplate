from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

from schemas import SelectionSchema, SelectionUpdateSchema
from utility.database import SQLHelper
from utility.exceptions import create_exceptions

selectionBlueprint = Blueprint("Selections", "selections", description="Operations on selections")


@selectionBlueprint.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify({
        "code": 422,
        "errors": error.messages,
        "status": "Unprocessable Entity"
    })
    response.status_code = 422
    return response


@selectionBlueprint.route("/selection")
class SelectionList(MethodView):
    @SQLHelper.handle_database_connection
    @create_exceptions
    @selectionBlueprint.arguments(SelectionSchema)
    @selectionBlueprint.response(201, SelectionSchema)
    def post(self, cursor, selection_data):

        cursor.execute(
            "INSERT INTO selection (name, event, price, active, outcome) "
            "VALUES (%s, %s, %s, %s, %s) "
            "RETURNING name, event, price, active, outcome;",
            (selection_data["name"], selection_data["event"], selection_data["price"], selection_data["active"],
             selection_data["outcome"]),
        )
        selection = cursor.fetchone()

        return jsonify(selection)

    @SQLHelper.handle_database_connection
    @selectionBlueprint.arguments(SelectionUpdateSchema)
    def put(self, cursor, sport_data):

        name = request.args.get('name')
        event = request.args.get('event')

        cursor.execute('SELECT * FROM selection WHERE name = %s AND event = %s', (name, event))
        selection = cursor.fetchone()

        if not selection:
            return jsonify({"error": "Selection not found."}), 404

        price = sport_data.get('price')
        active = sport_data.get('active')
        outcome = sport_data.get('outcome')

        if price is not None:
            update_query = 'UPDATE selection SET price = %s WHERE name = %s AND event = %s'
            cursor.execute(update_query, (price, name, event))

        if active is not None:
            update_query = 'UPDATE selection SET active = %s WHERE name = %s AND event = %s'
            cursor.execute(update_query, (active, name, event))
            if not active:
                cursor.execute(
                    """
                    SELECT COUNT(CASE WHEN se.active = FALSE THEN 1 END) AS inactive_count,
                           COUNT(*)                                     AS total_count
                    FROM event e
                    JOIN selection se on e.name = se.event
                    WHERE e.name = %s;

                    """, (event,))
                counter_results = cursor.fetchone()
                if counter_results["inactive_count"] == counter_results["total_count"]:
                    update_query = 'UPDATE event SET active = %s WHERE name = %s'
                    cursor.execute(update_query, (False, event))



        if outcome is not None:
            update_query = 'UPDATE selection SET outcome = %s WHERE name = %s AND event = %s '
            cursor.execute(update_query, (outcome, name, event))

        cursor.execute('SELECT * FROM selection WHERE name = %s AND event = %s', (name, event))
        selection_updated = cursor.fetchone()

        return jsonify(selection_updated)
