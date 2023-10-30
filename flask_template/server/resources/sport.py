from flask import jsonify, current_app
from flask.views import MethodView
from flask_smorest import Blueprint

from server.extensions.database import handle_database_connection
from server.schemas import SportSchema, SportUpdateSchema
from server.utility.exceptions import create_exceptions

sportBlueprint = Blueprint("Sports", "sports", description="Operations on sports")


@sportBlueprint.route("/sport/<string:sport_id>")
class Sport(MethodView):
    @sportBlueprint.response(200, SportSchema)
    @handle_database_connection
    def get(self, cursor, sport_id):
        cache = current_app.config["CACHE"]
        cached_sport = cache.get(sport_id)
        if cached_sport:
            return jsonify(cached_sport)

        cursor.execute('SELECT * FROM sport WHERE name = %s', (sport_id,))
        sport = cursor.fetchone()

        if sport is None:
            return jsonify({"error": "Sport not found"}), 404

        cache.set(sport_id, sport, timeout=60)
        return jsonify(sport)

    @handle_database_connection
    def delete(self, cursor, sport_id):

        cursor.execute('SELECT * FROM sport WHERE name = %s', (sport_id,))
        sport = cursor.fetchone()
        if not sport:
            return jsonify({"error": "Sport not found"}), 404
        delete_query = 'DELETE FROM sport WHERE name = %s'
        cursor.execute(delete_query, (sport_id,))

        return {"message": "Sport deleted."}

    @handle_database_connection
    @sportBlueprint.arguments(SportUpdateSchema)
    @sportBlueprint.response(200, SportSchema)
    def put(self, cursor, sport_data, sport_id):

        cursor.execute('SELECT * FROM sport WHERE name = %s', (sport_id,))
        sport = cursor.fetchone()
        if not sport:
            return jsonify({"error": "Sport not found"}), 404

        slug = sport_data.get('slug')
        active = sport_data.get('active')

        if slug is not None and active is not None:
            update_query = 'UPDATE sport SET slug = %s, active = %s WHERE name = %s RETURNING *'
            cursor.execute(update_query, (slug, active, sport_id))
        elif slug is not None:
            update_query = 'UPDATE sport SET slug = %s WHERE name = %s RETURNING *'
            cursor.execute(update_query, (slug, sport_id))
        elif active is not None:
            update_query = 'UPDATE sport SET active = %s WHERE name = %s RETURNING *'
            cursor.execute(update_query, (active, sport_id))
        updated_sport = cursor.fetchone()

        return jsonify(updated_sport)


@sportBlueprint.route("/sport")
class SportList(MethodView):
    @handle_database_connection
    @sportBlueprint.response(200, SportSchema(many=True))
    def get(self, cursor):
        cursor.execute('SELECT name, slug, active FROM sport')
        sports = cursor.fetchall()

        return jsonify(sports)

    @create_exceptions
    @sportBlueprint.arguments(SportSchema)
    @sportBlueprint.response(201, SportSchema)
    @handle_database_connection
    def post(self, cursor, sport_data):
        cursor.execute(
            "INSERT INTO sport (name, slug, active) VALUES (%s, %s, %s) RETURNING name, slug, active;",
            (sport_data["name"], sport_data["slug"], sport_data["active"]),
        )
        item = cursor.fetchone()

        return jsonify(item)
