from flask import jsonify
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from psycopg2.extras import RealDictCursor

from database import get_db
from schemas import SportSchema

sportBlueprint = Blueprint("Sports", "sports", description="Operations on sports")


@sportBlueprint.route("/sport/<string:name>")
class Sport(MethodView):
    @sportBlueprint.response(200, SportSchema)
    def get(self, name):

        db = get_db()
        cursor = db.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM sport WHERE name = %s', (name,))
        sport = cursor.fetchone()
        if sport is None:
            return jsonify({"error": "Sport not found"}), 404
        db.commit()
        cursor.close()

        return sport

    def delete(self, name):

        return {"message": "Item deleted."}

    @sportBlueprint.arguments(SportSchema)
    @sportBlueprint.response(200, SportSchema)
    def put(self, item_data, item_id):

        item = ""
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ""
            # item = ItemModel(id=item_id, **item_data)

        # db.session.add(item)
        # db.session.commit()

        return item


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

    @sportBlueprint.arguments(SportSchema)
    @sportBlueprint.response(201, SportSchema)
    def post(self, sport_data):
        item = {}

        try:

            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO sport (name, slug, active) VALUES (%s, %s, %s) RETURNING name, slug, active;",
                (sport_data["name"], sport_data["slug"], str(sport_data["active"])),
            )

            # Fetch the inserted item
            item = cursor.fetchone()
            db.commit()
            cursor.close()
        except Exception:
            abort(500, message="An error occurred while inserting the item.")

        return item
