"""This module is responsible for unittests of NumberConsumerCommand

"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import IntegrityError
from api.commands import NumberConsumerCommand
from api.settings import RABBITMQ_HOST, RABBITMQ_QUEUE


class NumberConsumerCommandTestCase(TestCase):
    """Class responsible for unittests of NumberConsumerCommand

    """

    @patch('api.commands.number_consumer.db')
    @patch('api.commands.number_consumer.NumbersModel')
    def test_callback(self, mock_numbers_model, mock_db):
        """Test callback method

        :param mock_numbers_model: The mock of NumbersModel
        :type mock_numbers_model: unittest.mock.MagicMock
        :param mock_db: The mock of db
        :type mock_db: unittest.mock.MagicMock
        """        
        mock_channel = MagicMock()
        mock_method = MagicMock()
        NumberConsumerCommand._callback(mock_channel, mock_method, MagicMock(), '1')
        mock_numbers_model.assert_called_once_with(number=1)
        mock_db.session.add.assert_called_once_with(mock_numbers_model.return_value)
        mock_db.session.commit.assert_called_once_with()
        mock_channel.basic_ack(delivery_tag=mock_method.delivery_tag)
        mock_numbers_model.reset_mock()
        mock_db.reset_mock()
        mock_channel.reset_mock()

        mock_db.session.commit.side_effect = IntegrityError(
            'UniqueViolation', 'mock', 'mock'
        )
        NumberConsumerCommand._callback(mock_channel, mock_method, MagicMock(), '1')
        mock_numbers_model.assert_called_once_with(number=1)
        mock_db.session.add.assert_called_once_with(mock_numbers_model.return_value)
        mock_db.session.commit.assert_called_once_with()
        mock_db.session.rollback.assert_called_once_with()
        mock_channel.basic_ack(delivery_tag=mock_method.delivery_tag)
        mock_numbers_model.reset_mock()
        mock_db.reset_mock()
        mock_channel.reset_mock()

        mock_db.session.commit.side_effect = IntegrityError(
            'mock', 'mock', 'mock'
        )
        self.assertRaises(
            IntegrityError, NumberConsumerCommand._callback,
            mock_channel, mock_method, MagicMock(), '1'
        )
        mock_numbers_model.assert_called_once_with(number=1)
        mock_db.session.add.assert_called_once_with(mock_numbers_model.return_value)
        mock_db.session.commit.assert_called_once_with()
        mock_db.session.rollback.assert_called_once_with()
        mock_channel.basic_ack(delivery_tag=mock_method.delivery_tag)

    @staticmethod
    @patch('pika.ConnectionParameters')
    @patch('pika.BlockingConnection')
    def test_run(mock_blocking_connection, mock_connection_parameters):
        """Test run method

        :param mock_blocking_connection: The mock of pika.BlockingConnection
        :type mock_blocking_connection: unittest.mock.MagicMock
        :param mock_connection_parameters: The mock of pika.ConnectionParameters
        :type mock_connection_parameters: unittest.mock.MagicMock
        """
        NumberConsumerCommand().run()
        mock_connection_parameters.assert_called_once_with(host=RABBITMQ_HOST)
        mock_blocking_connection.assert_called_once_with(
            mock_connection_parameters.return_value
        )
        mock_blocking_connection.return_value.channel.assert_called_once_with()
        mock_blocking_connection.return_value.channel.return_value. \
            queue_declare.assert_called_once_with(
                queue=RABBITMQ_QUEUE
            )
        mock_blocking_connection.return_value.channel.return_value. \
            basic_consume.assert_called_once_with(
                on_message_callback=NumberConsumerCommand._callback, queue=RABBITMQ_QUEUE
            )
        mock_blocking_connection.return_value.channel.return_value. \
            start_consuming.assert_called_once_with()
        mock_blocking_connection.return_value.channel.return_value. \
            close.assert_called_once_with()
        mock_blocking_connection.return_value.close.assert_called_once_with()
