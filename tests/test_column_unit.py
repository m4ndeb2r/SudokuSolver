import unittest
from unittest.mock import Mock

from board.board_exception import BoardException
from board.column_unit import ColumnUnit


class TestColumnUnit(unittest.TestCase):

    __board_mock = Mock()

    def test_init_invalid_colum_unit(self):
        cell_keys_for_a_row = [
            "x1y9", "x2y9", "x3y9",
            "x4y9", "x5y9", "x6y9",
            "x7y9", "x8y9", "x9y9",
        ]
        with self.assertRaises(BoardException) as context:
            ColumnUnit(self.__board_mock, cell_keys_for_a_row)
        self.assertTrue("Not a valid column; cell keys do not align" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
