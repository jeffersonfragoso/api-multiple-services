"""This package is responsible for the number generator

"""

import logging
import random
import pika
from service import settings

LOGGER = logging.getLogger(__name__)


class GenerateNumbersService:  # pylint: disable=too-few-public-methods
    """Class responsible for the number generator

    """

    @staticmethod
    def _generate_number():
        """Generate number

        :return: The number generated
        :rtype: int
        """
        while True:
            number = random.randint(settings.RANGE_MIN, settings.RANGE_MAX)
            if settings.NUMBER_TYPE == 'even' and number % 2 == 0:
                return number
            if settings.NUMBER_TYPE == 'odd' and number % 2 != 0:
                return number

    @classmethod
    def _callback(cls, channel, method, properties, _body):
        """Callback function to received new messages from the broker

        :param channel: The channel
        :type channel: pika.Channel
        :param method: The method
        :type method: pika.spec.Basic.Deliver
        :param properties: The properties
        :type properties: pika.spec.BasicProperties
        :param _body: The body
        :type _body: bytes
        """
        LOGGER.debug('Generate a new number with type %s', settings.NUMBER_TYPE)
        number = cls._generate_number()
        LOGGER.debug('Publish the number %s to the %s', number, properties.reply_to)
        channel.basic_publish(
            exchange='', routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=str(number)
        )
        LOGGER.debug('Sending basic ack')
        channel.basic_ack(delivery_tag=method.delivery_tag)

    @classmethod
    def run(cls):
        """Creating the queue and starting consume messages from this queue

        """
        LOGGER.debug('Creating connection with RabbitMQ host %s', settings.RABBITMQ_HOST)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        LOGGER.debug('Creating channel')
        channel = connection.channel()
        LOGGER.debug('Declare the queue %s', settings.RABBITMQ_QUEUE)
        channel.queue_declare(queue=settings.RABBITMQ_QUEUE)
        LOGGER.debug('Registering the callback function for queue %s', settings.RABBITMQ_QUEUE)
        channel.basic_consume(on_message_callback=cls._callback, queue=settings.RABBITMQ_QUEUE)
        LOGGER.debug('Starting consuming the queue')
        channel.start_consuming()
        LOGGER.debug('Closing channel')
        channel.close()
        LOGGER.debug('Closing connection')
        connection.close()


if __name__ == '__main__':
    service = GenerateNumbersService()
    service.run()
