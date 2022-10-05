import traceback

from dotenv import dotenv_values
from flask import Flask
from marshmallow import ValidationError
from flask_cors import CORS

import cocktail_maker.db.models
from cocktail_maker.db import create_db, db
from flask_migrate import Migrate
from cocktail_maker.routes import load_routes

migrate = Migrate()


def create_app(env_file='.env') -> Flask:
    env_config = dotenv_values(env_file)
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, send_wildcard=True)
    app.config.from_object(env_config)
    app.config['SQLALCHEMY_DATABASE_URI'] = env_config.get(
        'SQLALCHEMY_DATABASE_URI')
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        load_routes(app, env_config)

        @app.errorhandler(ValidationError)
        def register_validation_error(error):
            rv = dict({'message': error.messages})
            return rv, 400

        @app.errorhandler(Exception)
        def register_any_error(error):
            rv = dict({'message': traceback.format_exc()})
            return rv, 500

        # db.drop_all()
        db.create_all()
        return app


app = create_app()

if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
