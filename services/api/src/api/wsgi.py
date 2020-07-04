"""This module is responsible for create the app for gunicorn

"""

from api.app import create_app
APP = create_app()
