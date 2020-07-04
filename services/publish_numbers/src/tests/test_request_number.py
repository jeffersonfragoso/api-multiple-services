"""This module is responsible for unittest of RequestNumber class

"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from service import settings
from service.request_number import RequestNumber


class RequestNumberTestCase(TestCase):
    """Class responsible for all unittests of RequestNumber

    """

    def setUp(self):
        """Creating RequestNumber instance

        """
        with patch('pika.BlockingConnection') as mock_blocking_connection, \
                patch('pika.ConnectionParameters') as mock_connection_parameters, \
                patch('pika.BasicProperties') as mock_basic_properties, \
                patch('uuid.uuid4') as mock_uuid:
            self.request = RequestNumber('test')
            mock_connection_parameters.assert_called_once_with(host=settings.RABBITMQ_HOST)
            mock_blocking_connection.assert_called_once_with(
                mock_connection_parameters.return_value
            )
            mock_blocking_connection.return_value.channel.assert_called_once_with()
            mock_blocking_connection.return_value.channel.return_value. \
                queue_declare.assert_called_once_with(
                    queue='', exclusive=True
                )
            mock_blocking_connection.return_value.channel.return_value. \
                basic_consume.assert_called_once_with(
                    on_message_callback=self.request._callback,
                    queue=mock_blocking_connection.return_value.channel.
                    return_value.queue_declare.return_value.method.queue,
                    auto_ack=True
                )
            mock_basic_properties.assert_called_once_with(
                reply_to=mock_blocking_connection.return_value.channel.
                return_value.queue_declare.return_value.method.queue,
                correlation_id=str(mock_uuid.return_value)
            )

    def test_callback(self):
        """Test callback method

        """
        mock_properties = MagicMock(correlation_id=self.request._correlation_id)
        self.request._callback(MagicMock(), MagicMock(), mock_properties, '1')
        self.assertEqual(self.request._number, 1)

        mock_properties = MagicMock(correlation_id='invalid')
        self.request._number = None
        self.request._callback(MagicMock(), MagicMock(), mock_properties, '1')
        self.assertIsNone(self.request._number)

    def test_gen(self):
        """Test gen method

        """
        self.assertIsNone(self.request.gen(timeout=10))
        self.request._channel.basic_publish.assert_called_once_with(
            exchange='', routing_key=self.request._queue, body='',
            properties=self.request._properties
        )
        self.request._connection.process_data_events.assert_called_once_with(
            time_limit=10
        )

    def test_close(self):
        """Test close method

        """
        self.request.close()
        self.request._channel.close.assert_called_once_with()
        self.request._connection.close.assert_called_once_with()