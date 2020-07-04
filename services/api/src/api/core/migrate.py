"""This module is responsible for create the migrate object

"""

# pylint: disable=invalid-name

from flask_migrate import Migrate
from .database import db

migrate = Migrate()


def init_migrate(app):
    """Init the migrate

    :param app: The flask app
    :type app: Flask
    """
    migrate.init_app(app, db)
