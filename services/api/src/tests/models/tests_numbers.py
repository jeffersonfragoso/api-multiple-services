"""This module is responsible for unittests of NumbersModel

"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from api.models import NumbersModel


class NumbersModelTestCase(TestCase):
    """Class responsible for unittests of NumbersModel

    """

    def test_get_numbers(self):
        """Test get numbers method

        """
        NumbersModel.query = MagicMock()
        self.assertTupleEqual(
            NumbersModel.get_numbers(),
            (
                NumbersModel.query.count.return_value,
                NumbersModel.query.offset.return_value.limit.return_value
            )
        )
        NumbersModel.query.count.assert_called_once_with()
        NumbersModel.query.offset.assert_called_once_with(0)
        NumbersModel.query.offset.return_value.limit.assert_called_once_with(20)
