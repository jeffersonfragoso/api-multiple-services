"""This package has all configuration.

"""

import os

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_QUEUE = os.environ.get('RABBITMQ_QUEUE')
NUMBER_TYPE = os.environ.get('NUMBER_TYPE')
RANGE_MIN = int(os.environ.get('RANGE_MIN', '0'))
RANGE_MAX = int(os.environ.get('RANGE_MAX', '1000'))
