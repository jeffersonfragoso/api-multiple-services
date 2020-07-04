"""
This module has the settings of project
"""

import json
import os


# Logging configuration
LOGGING_FILE = os.path.join(os.path.dirname(__file__), 'logging.json')
LOGGING_CONFIG = None
with open(LOGGING_FILE) as config:
    LOGGING_CONFIG = json.load(config)

# Database settings
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'database')
DATABASE_USER = os.environ.get('DATABASE_USER', 'postgres')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'postgres')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'postgres')
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=DATABASE_USER, pw=DATABASE_PASSWORD, url=DATABASE_HOST, db=DATABASE_NAME
)

# RabbitMQ settings
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_QUEUE = os.environ.get('RABBITMQ_QUEUE', 'publish_numbers')
