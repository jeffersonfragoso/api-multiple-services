"""This package is responsible for request number to the service

"""

import logging
import uuid
import pika
from .settings import RABBITMQ_HOST

LOGGER = logging.getLogger(__name__)


class RequestNumber:  # pylint: disable=too-few-public-methods
    """Class responsible for request number to the service

    """

    def __init__(self, queue):
        """Create the Resquest Number instance

        :param queue: The queue to request number
        :type queue: str
        """
        LOGGER.debug('Creating connection with RabbitMQ host %s', RABBITMQ_HOST)
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        LOGGER.debug('Creating channel')
        self._channel = self._connection.channel()
        LOGGER.debug('Declare the queue')
        result = self._channel.queue_declare(queue='', exclusive=True)
        LOGGER.debug('Setting callback queue')
        self._callback_queue = result.method.queue
        LOGGER.debug('Registering the callback function for queue %s', self._callback_queue)
        self._channel.basic_consume(
            on_message_callback=self._callback, queue=self._callback_queue, auto_ack=True
        )
        LOGGER.debug('Setting correlanton id')
        self._correlation_id = str(uuid.uuid4())
        LOGGER.debug(
            'Creating properties with reply_to %s and correlation_id %s',
            self._callback_queue, self._correlation_id
        )
        self._properties = pika.BasicProperties(
            reply_to=self._callback_queue, correlation_id=self._correlation_id
        )
        self._queue = queue
        self._number = None

    def _callback(self, _channel, _method, properties, body):
        """Callback function to received new messages from the broker

        :param _channel: The channel
        :type _channel: pika.Channel
        :param _method: The method
        :type _method: pika.spec.Basic.Deliver
        :param properties: The properties
        :type properties: pika.spec.BasicProperties
        :param body: The body
        :type body: bytes
        """
        if self._correlation_id == properties.correlation_id:
            self._number = int(body)

    def gen(self, timeout=0):
        """Request to generate the number

        :param timeout: The timeout, defaults to 0
        :type timeout: int, optional
        :return: The number that was generated
        :rtype: int
        """
        self._number = None

        LOGGER.debug('Publish message to the queue %s', self._queue)
        self._channel.basic_publish(
            exchange='', routing_key=self._queue, body='', properties=self._properties
        )

        LOGGER.debug('Waiting %s for receive the number', timeout)
        self._connection.process_data_events(time_limit=timeout)

        return self._number

    def close(self):
        """Close channel and connection

        """
        LOGGER.debug('Closing channel')
        self._channel.close()
        LOGGER.debug('Closing connection')
        self._connection.close()
