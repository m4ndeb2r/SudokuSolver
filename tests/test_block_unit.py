import unittest
from unittest.mock import Mock

from board.block_unit import BlockUnit
from board.board_exception import BoardException


class TestBlockUnit(unittest.TestCase):

    __board_mock = Mock()

    def test_init_invalid_block_unit(self):
        cell_keys_for_a_row = [
            "x1y1", "x2y1", "x3y1",
            "x4y1", "x5y1", "x6y1",
            "x7y1", "x8y1", "x9y1",
        ]
        with self.assertRaises(BoardException) as context:
            BlockUnit(self.__board_mock, cell_keys_for_a_row)
        self.assertTrue("Not a valid block" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
