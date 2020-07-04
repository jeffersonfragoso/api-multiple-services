"""This package is responsible for the publish numbers

"""

import logging
import time
import pika
from .request_number import RequestNumber
from .settings import (
    RABBITMQ_HOST, RABBITMQ_EVEN_QUEUE, RABBITMQ_ODD_QUEUE, RABBITMQ_PUBLISH_QUEUE,
    PUBLISH_TIME_MS, PUBLISH_MIN_NUMBER
)

LOGGER = logging.getLogger(__name__)


class PublishNumbersService:  # pylint: disable=too-few-public-methods
    """Class responsible for publish numbers

    """

    @staticmethod
    def run():
        """Request even number and odd number than multiple this two numbers
        and publish numbers bigger than PUBLISH_MIN_NUMBER

        """
        LOGGER.debug('Creating even number request')
        even_request = RequestNumber(RABBITMQ_EVEN_QUEUE)
        LOGGER.debug('Creating odd number request')
        odd_request = RequestNumber(RABBITMQ_ODD_QUEUE)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_PUBLISH_QUEUE)

        while True:
            try:
                even_number = even_request.gen(timeout=5)
                if even_number is None:
                    LOGGER.debug('Received a invalid number from even number service')
                    continue

                odd_number = odd_request.gen(timeout=5)
                if odd_number is None:
                    LOGGER.debug('Received a invalid number from odd number service')
                    continue

                multiplication = even_number * odd_number
                if multiplication > PUBLISH_MIN_NUMBER:
                    LOGGER.debug(
                        'Publishing the number %s to the queue %s',
                        multiplication, RABBITMQ_PUBLISH_QUEUE
                    )
                    channel.basic_publish(
                        exchange='', routing_key=RABBITMQ_PUBLISH_QUEUE, body=str(multiplication)
                    )

                time.sleep(PUBLISH_TIME_MS / 1000)
            except KeyboardInterrupt:
                break

        LOGGER.debug('Closing even request')
        even_request.close()
        LOGGER.debug('Closing odd request')
        odd_request.close()
        LOGGER.debug('Closing channel')
        channel.close()
        LOGGER.debug('Closing connection')
        connection.close()


if __name__ == '__main__':
    service = PublishNumbersService()
    service.run()
