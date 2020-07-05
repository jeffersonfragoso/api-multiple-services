"""This module is responsible for consume the publish numbers from RabbitMQ

"""

import logging
import pika
from sqlalchemy.exc import IntegrityError
from flask_script import Command
from api.core.database import db
from api.models import NumbersModel
from api.settings import RABBITMQ_HOST, RABBITMQ_QUEUE

LOGGER = logging.getLogger(__name__)


class NumberConsumerCommand(Command):
    """Class responsible for consume the publish number and insert into database

    """

    @staticmethod
    def _callback(channel, method, _properties, body):
        """Callback function to received new messages from the broker

        :param channel: The channel
        :type channel: pika.Channel
        :param method: The method
        :type method: pika.spec.Basic.Deliver
        :param _properties: The properties
        :type _properties: pika.spec.BasicProperties
        :param body: The body
        :type body: bytes
        """
        try:
            LOGGER.debug('Creating the new number model with number %s', body)
            number = NumbersModel(number=int(body))
            LOGGER.debug('Adding the number in database')
            db.session.add(number)
            LOGGER.debug('Commiting the new number')
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            if 'UniqueViolation' not in str(error):
                raise
            LOGGER.debug('The number %s already exists in database, skip')

        LOGGER.debug('Sending basic ack')
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        """Starting consuming the publish numbers

        """
        LOGGER.debug('Creating connection with RabbitMQ host %s', RABBITMQ_HOST)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        LOGGER.debug('Creating channel')
        channel = connection.channel()
        LOGGER.debug('Declare the queue %s', RABBITMQ_QUEUE)
        channel.queue_declare(queue=RABBITMQ_QUEUE)
        LOGGER.debug('Registering the callback function for queue %s', RABBITMQ_QUEUE)
        channel.basic_consume(on_message_callback=self._callback, queue=RABBITMQ_QUEUE)
        LOGGER.debug('Starting consuming the queue')
        channel.start_consuming()
        LOGGER.debug('Closing channel')
        channel.close()
        LOGGER.debug('Closing connection')
        connection.close()
