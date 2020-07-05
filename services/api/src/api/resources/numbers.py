"""This package has the implementation of Numbers Resources

"""

from flask_restful import Resource, reqparse
from flasgger.utils import swag_from
from api.models import NumbersModel


class NumbersResource(Resource):
    """The Numbers Resource class is responsible for list all numbers in the database

    """

    def __init__(self):
        """Create the Numbers Resource instance

        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('offset', type=str, default=0)
        self.parser.add_argument('limit', type=str, default=20)

    @swag_from('numbers.yaml')
    def get(self):
        """Get list of numbers

        :return: The data with the count o numbers and the list of numbers for the current page
        :rtype: dict
        """
        args = self.parser.parse_args()
        print(args)
        count, query = NumbersModel.get_numbers(**args)
        return {
            'count': count, 'data': [model.number for model in query]
        }
