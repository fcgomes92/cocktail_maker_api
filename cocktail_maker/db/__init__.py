from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_db(app, config):
    return db
