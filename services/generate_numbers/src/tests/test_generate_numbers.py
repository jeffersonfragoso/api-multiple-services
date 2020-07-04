"""This module is responsible for unittest of GenerateNumbersService class

"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from service.generate_numbers import GenerateNumbersService
from service.settings import RABBITMQ_HOST, RABBITMQ_QUEUE


class GenerateNumbersServiceTestCase(TestCase):
    """Class responsible for all unittests of GenerateNumbersService

    """

    @patch('service.generate_numbers.settings')
    def test_generate_number_even(self, mock_settings):
        """Test generate even number method

        :param mock_settings: The mock of settings
        :type mock_settings: unittest.mock.MagicMock
        """
        mock_settings.NUMBER_TYPE = 'even'
        mock_settings.RANGE_MIN = 0
        mock_settings.RANGE_MAX = 100

        number = GenerateNumbersService._generate_number()
        self.assertGreaterEqual(number, mock_settings.RANGE_MIN)
        self.assertLessEqual(number, mock_settings.RANGE_MAX)
        self.assertEqual(number % 2, 0)

    @patch('service.generate_numbers.settings')
    def test_generate_number_odd(self, mock_settings):
        """Test generate odd number method

        :param mock_settings: The mock of settings
        :type mock_settings: unittest.mock.MagicMock
        """
        mock_settings.NUMBER_TYPE = 'odd'
        mock_settings.RANGE_MIN = 0
        mock_settings.RANGE_MAX = 100

        number = GenerateNumbersService._generate_number()
        self.assertGreaterEqual(number, mock_settings.RANGE_MIN)
        self.assertLessEqual(number, mock_settings.RANGE_MAX)
        self.assertNotEqual(number % 2, 0)

    @staticmethod
    @patch('pika.BasicProperties')
    @patch.object(GenerateNumbersService, '_generate_number')
    def test_callback(mock_generate_even_number, mock_basic_properties):
        """Test callbakc method

        :param mock_generate_even_number: The mock of GenerateNumbersService _generate_number
        :type mock_generate_even_number: unittest.mock.MagicMock
        :param mock_basic_properties: The mock of pika.BasicProperties
        :type mock_basic_properties: unittest.mock.MagicMock
        """
        mock_channel = MagicMock()
        mock_method = MagicMock()
        mock_properties = MagicMock()

        GenerateNumbersService._callback(mock_channel, mock_method, mock_properties, MagicMock())
        mock_basic_properties.assert_called_once_with(
            correlation_id=mock_properties.correlation_id
        )
        mock_channel.basic_publish.assert_called_once_with(
            exchange='', routing_key=mock_properties.reply_to,
            properties=mock_basic_properties.return_value,
            body=str(mock_generate_even_number.return_value)
        )
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
        GenerateNumbersService.run()
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
                on_message_callback=GenerateNumbersService._callback, queue=RABBITMQ_QUEUE
            )
        mock_blocking_connection.return_value.channel.return_value. \
            start_consuming.assert_called_once_with()
