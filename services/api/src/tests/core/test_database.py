"""This module has all tests of database module

"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from api.core.database import init_database
from api.settings import DB_URL


class DatabseTestCase(TestCase):
    """Class responsible for all tests of database

    """

    @patch('api.core.database.db')
    def test_init_database(self, mock_db):
        """Test init database method

        :param mock_db: The mock of database
        :type mock_db: unittest.mock.MagicMock
        """
        mock_app = MagicMock()
        mock_app.config = {}

        init_database(mock_app)

        self.assertEqual(
            mock_app.config['SQLALCHEMY_DATABASE_URI'],
            DB_URL
        )
        self.assertEqual(
            mock_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'],
            False
        )

        mock_db.init_app.assert_called_once_with(mock_app)
