import unittest
from unittest.mock import Mock

from board.board_exception import BoardException
from board.row_unit import RowUnit


class TestRowUnit(unittest.TestCase):

    __board_mock = Mock()

    def test_init_invalid_row_unit(self):
        cell_keys_for_a_column = [
            "x1y1", "x1y2", "x1y2",
            "x1y4", "x1y5", "x1y6",
            "x1y7", "x1y8", "x1y9",
        ]
        with self.assertRaises(BoardException) as context:
            RowUnit(self.__board_mock, cell_keys_for_a_column)
        self.assertTrue("Not a valid row; cell keys do not align" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
