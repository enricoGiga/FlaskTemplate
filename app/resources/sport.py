from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from psycopg2.extras import RealDictCursor

from database import get_db
from exceptions import create_exceptions
from schemas import SportSchema, SportUpdateSchema

sportBlueprint = Blueprint("Sports", "sports", description="Operations on sports")


@sportBlueprint.route("/sport/<string:sport_id>")
class Sport(MethodView):
    @sportBlueprint.response(200, SportSchema)
    def get(self, sport_id):

        db = get_db()
        cursor = db.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM sport WHERE name = %s', (sport_id,))
        sport = cursor.fetchone()
        if sport is None:
            return jsonify({"error": "Sport not found"}), 404
        db.commit()
        cursor.close()

        return sport

    def delete(self, sport_id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM sport WHERE name = %s', (sport_id,))
            sport = cursor.fetchone()

            if not sport:
                db.commit()
                cursor.close()
                abort(404, message='Sport not found.')

            delete_query = 'DELETE FROM sport WHERE name = %s'
            cursor.execute(delete_query, (sport_id,))

            db.commit()
            cursor.close()
        return {"message": "Sport deleted."}

    @sportBlueprint.arguments(SportUpdateSchema)
    @sportBlueprint.response(200, SportSchema)
    def put(self, sport_data, sport_id):
        db = get_db()
        cursor = db.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM sport WHERE name = %s', (sport_id,))
        sport = cursor.fetchone()
        if not sport:
            db.commit()
            cursor.close()
            abort(404, message='Sport not found.')
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
        db.commit()
        cursor.close()

        return updated_sport


@sportBlueprint.route("/sport")
class SportList(MethodView):
    @sportBlueprint.response(200, SportSchema(many=True))
    def get(self):
        db = get_db()
        cursor = db.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT name, slug, active FROM sport')
        sports = cursor.fetchall()
        db.commit()
        cursor.close()

        return sports

    @create_exceptions
    @sportBlueprint.arguments(SportSchema)
    @sportBlueprint.response(201, SportSchema)
    def post(self, sport_data):
        db = get_db()
        cursor = db.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "INSERT INTO sport (name, slug, active) VALUES (%s, %s, %s) RETURNING name, slug, active;",
            (sport_data["name"], sport_data["slug"], sport_data["active"]),
        )

        item = cursor.fetchone()
        db.commit()
        cursor.close()

        return item
