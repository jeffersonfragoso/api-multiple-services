"""This module is responsible for create the database object

"""

# pylint: disable=invalid-name

from flask_sqlalchemy import SQLAlchemy
from api.settings import DB_URL

db = SQLAlchemy()


def init_database(app):
    """Init the database

    :param app: The flask app
    :type app: Flask
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
