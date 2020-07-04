"""This module is responsible for unittest of PublishNumbersService class

"""

from unittest import TestCase
from unittest.mock import call, patch
from service import settings
from service.publish_numbers import PublishNumbersService


class PublishNumbersServiceTestCase(TestCase):
    """Class responsible for all unittests of PublishNumbersService

    """

    @staticmethod
    @patch('time.sleep')
    @patch('pika.ConnectionParameters')
    @patch('pika.BlockingConnection')
    @patch('service.publish_numbers.RequestNumber')
    def test_run(mock_request_number, mock_blocking_connection,
                 mock_connection_parameters, mock_time_sleep):
        """Test run method

        :param mock_request_number: The mock of RequestNumber
        :type mock_request_number: unittest.mock.MagicMock
        :param mock_blocking_connection: The mock of pika.BlockingConnection
        :type mock_blocking_connection: unittest.mock.MagicMock
        :param mock_connection_parameters: The mock of pika.ConnectionParameters
        :type mock_connection_parameters: unittest.mock.MagicMock
        :param mock_time_sleep: The mock of time.sleep
        :type mock_time_sleep: unittest.mock.MagicMock
        """
        mock_request_number.return_value.gen.side_effect = [
            998, 887, KeyboardInterrupt()
        ]
        PublishNumbersService.run()
        mock_request_number.assert_has_calls([
            call(settings.RABBITMQ_EVEN_QUEUE), call(settings.RABBITMQ_ODD_QUEUE)
        ])
        mock_connection_parameters.assert_called_once_with(host=settings.RABBITMQ_HOST)
        mock_blocking_connection.assert_called_once_with(
            mock_connection_parameters.return_value
        )
        mock_blocking_connection.return_value.channel.assert_called_once_with()
        mock_blocking_connection.return_value.channel.return_value. \
            queue_declare.assert_called_once_with(
                queue=settings.RABBITMQ_PUBLISH_QUEUE
            )
        mock_request_number.return_value.gen.assert_has_calls([
            call(timeout=5), call(timeout=5), call(timeout=5)
        ])
        mock_blocking_connection.return_value.channel.return_value. \
            basic_publish.assert_called_once_with(
                exchange='', routing_key=settings.RABBITMQ_PUBLISH_QUEUE,
                body=str(998*887)
            )
        mock_time_sleep.assert_called_once_with(settings.PUBLISH_TIME_MS/1000)
        mock_request_number.return_value.close.assert_has_calls([
            call(), call()
        ])
        mock_blocking_connection.return_value.channel.return_value. \
            close.assert_called_once_with()
        mock_blocking_connection.return_value.close.assert_called_once_with()
