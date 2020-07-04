"""The main module

"""

import os
import json
import logging
import logging.config
from .publish_numbers import PublishNumbersService

LOGGER = logging.getLogger(__name__)


def main():
    """This is the main function of app

    :return: The exit code value
    :rtype: int
    """
    config_path = os.path.join(os.path.dirname(__file__), 'logging.json')
    with open(config_path, 'r', encoding='utf-8') as config:
        logging.config.dictConfig(json.load(config))

    service = PublishNumbersService()
    service.run()


if __name__ == "__main__":
    main()
