"""The manage commands of API

"""

import importlib
import logging.config
from flask_migrate import MigrateCommand
from flask_script import Manager, Command
from api.app import create_app
from api.commands import NumberConsumerCommand
from api.settings import LOGGING_CONFIG

APP = create_app()
MANAGER = Manager(app=APP)

MANAGER.add_command('db', MigrateCommand)
MANAGER.add_command('number_consumer', NumberConsumerCommand)

if __name__ == '__main__':
    LOGGING_CONFIG['loggers'] = {'api.commands': {
        'handlers': ['console'],
        'level': 'DEBUG'
    }}
    logging.config.dictConfig(LOGGING_CONFIG)
    MANAGER.run()
