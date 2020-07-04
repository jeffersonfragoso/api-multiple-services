"""This package has all configuration.

"""

import os

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_EVEN_QUEUE = os.environ.get('RABBITMQ_EVEN_QUEUE', 'even_numbers')
RABBITMQ_ODD_QUEUE = os.environ.get('RABBITMQ_ODD_QUEUE', 'odd_numbers')
RABBITMQ_PUBLISH_QUEUE = os.environ.get('RABBITMQ_PUBLISH_QUEUE', 'publish_numbers')
PUBLISH_TIME_MS = int(os.environ.get('PUBLISH_TIME_MS', '500'))
PUBLISH_MIN_NUMBER = int(os.environ.get('PUBLISH_MIN_NUMBER', '100000'))
