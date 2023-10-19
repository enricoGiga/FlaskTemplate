import os

import psycopg2
from flask import Flask, g
from flask_smorest import Api, Blueprint

from resources.sport import sportBlueprint


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

    @app.teardown_appcontext
    def close_db_connection(exception=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    api = Api(app)

    api.register_blueprint(sportBlueprint)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
