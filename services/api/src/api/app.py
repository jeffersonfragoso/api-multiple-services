"""
This module has the App, Database configurations and Routes of API

"""

import logging
from flask import Flask
from flask_restful import Api
from api.resources import NumbersResource

LOGGER = logging.getLogger(__name__)


def create_app():
    """Create the flask app

    :return: The flask app
    :rtype: Flask
    """
    # pylint: disable=import-outside-toplevel

    LOGGER.debug('Creating the Api APP')

    flask_app = Flask(__name__)
    flask_api = Api(flask_app)

    from api.core.database import init_database
    init_database(flask_app)

    from api.core.migrate import init_migrate
    init_migrate(flask_app)

    flask_api.add_resource(NumbersResource, '/numbers')

    return flask_app
