"""This module has all tests of migrate module

"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from api.core.migrate import init_migrate


class DatabseTestCase(TestCase):
    """Class responsible for all tests of migrate

    """

    @patch('api.core.migrate.db')
    @patch('api.core.migrate.migrate')
    def test_init_database(self, mock_migrate, mock_db):
        """Test init database method

        :param mock_migrate: The mock of migrate
        :type mock_migrate: unittest.mock.MagicMock
        :param mock_db: The mock of db
        :type mock_db: unittest.mock.MagicMock
        """
        mock_app = MagicMock()

        init_migrate(mock_app)

        mock_migrate.init_app.assert_called_once_with(
            mock_app, mock_db
        )
