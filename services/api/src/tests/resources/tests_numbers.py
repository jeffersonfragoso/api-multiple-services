"""This module is responsible for unittests of NumbersResource

"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from api.resources import NumbersResource
from api.app import create_app

APP = create_app()


class NumbersResourceTestCase(TestCase):
    """Class responsible for unittests of NumbersResource

    """

    def setUp(self):
        """Create the test client

        """
        self.client = APP.test_client()

    @patch('api.resources.numbers.NumbersModel')
    def test_get(self, mock_numbers_models):
        """Test get method

        :param mock_numbers_model: The mock of NumbersModel
        :type mock_numbers_model: unittest.mock.MagicMock
        """
        mock_numbers_models.get_numbers.return_value = (1, [MagicMock(number=1)])
        response = self.client.get('/numbers')
        self.assertEqual(
            response.json, {'count': 1, 'data': [1]}
        )
        mock_numbers_models.get_numbers.assert_called_once_with(offset=0, limit=20)