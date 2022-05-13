import unittest

from board import Board
from unit import Unit
from exceptions import SudokuException


class TestUnit(unittest.TestCase):

    def test_init_valid_block_unit(self):
        board = Board()
        cell_keys = [
            "x4y1", "x5y1", "x6y1",
            "x4y2", "x5y2", "x6y2",
            "x4y3", "x5y3", "x6y3",
        ]
        unit = Unit(board, cell_keys, "block")
        self.assertTrue(unit.is_block_unit())

    def test_init_valid_row_unit(self):
        board = Board()
        cell_keys = [
            "x1y1", "x2y1", "x3y1",
            "x4y1", "x5y1", "x6y1",
            "x7y1", "x8y1", "x9y1",
        ]
        unit = Unit(board, cell_keys, "row")
        self.assertTrue(unit.is_row_unit())

    def test_init_valid_column_unit(self):
        board = Board()
        cell_keys = [
            "x1y1", "x1y2", "x1y2",
            "x1y4", "x1y5", "x1y6",
            "x1y7", "x1y8", "x1y9",
        ]
        unit = Unit(board, cell_keys, "column")
        self.assertTrue(unit.is_column_unit())

    def test_init_illegal_unit_type(self):
        with self.assertRaises(SudokuException) as context:
            Unit(Board(), [], "wrong_type")
        self.assertTrue("Illegal unit type: 'wrong_type'." in str(context.exception))

    def test_init_invalid_nr_of_cell_keys(self):
        with self.assertRaises(SudokuException) as context:
            Unit(Board(), ["x1y7", "x1y8", "x1y9"], "block")
        self.assertTrue("Not a valid block: ['x1y7', 'x1y8', 'x1y9']." in str(context.exception))


if __name__ == '__main__':
    unittest.main()
