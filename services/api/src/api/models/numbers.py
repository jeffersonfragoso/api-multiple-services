"""The Numbers model

"""

from api.core.database import db


class NumbersModel(db.Model):  # pylint: disable=too-few-public-methods
    """The Numbers model class

    """

    __tablename__ = 'numbers'

    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)

    @classmethod
    def get_numbers(cls, offset=0, limit=20):
        """Get the numbers

        :param offset: The offset, defaults to 0
        :type offset: int, optional
        :param limit: The limit, defaults to 20
        :type limit: int, optional
        :return: The tupple with the count of numbers and the numbers model
        :rtype: tupple
        """
        return cls.query.count(), cls.query.offset(offset).limit(limit)
