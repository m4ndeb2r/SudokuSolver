import unittest
from unittest.mock import Mock, call

from board.unit import Unit
from board.board_exception import BoardException


class TestUnit(unittest.TestCase):

    __board_mock = Mock()

    def test_init_illegal_unit_type(self):
        cell_keys = [
            "x4y1", "x5y1", "x6y1",
            "x4y2", "x5y2", "x6y2",
            "x4y3", "x5y3", "x6y3",
        ]
        with self.assertRaises(BoardException) as context:
            Unit(self.__board_mock, cell_keys, "wrong_type")
        self.assertTrue("Illegal unit type: 'wrong_type'." in str(context.exception))

    def test_init_invalid_nr_of_cell_keys(self):
        with self.assertRaises(BoardException) as context:
            Unit(self.__board_mock, ["x1y7", "x1y8", "x1y9"], "block")
        self.assertTrue("Not a valid unit: ['x1y7', 'x1y8', 'x1y9']." in str(context.exception))

    def test_init_invalid_cell_keys(self):
        invalid_cell_keys = [
            "x0y1", "x0y1", "x0y1",
            "x0y2", "x0y2", "x0y2",
            "x0y3", "x0y3", "x0y3",
        ]
        with self.assertRaises(BoardException) as context:
            Unit(self.__board_mock, invalid_cell_keys, "column")
        self.assertTrue("Not a valid unit; one or more keys not valid: " in str(context.exception))

    def test_init_valid_block_unit(self):
        cell_keys = [
            "x4y1", "x5y1", "x6y1",
            "x4y2", "x5y2", "x6y2",
            "x4y3", "x5y3", "x6y3",
        ]
        unit = Unit(self.__board_mock, cell_keys, "block")
        self.assertTrue(unit.is_block_unit())

    def test_init_invalid_block_unit(self):
        cell_keys_for_a_row = [
            "x1y1", "x2y1", "x3y1",
            "x4y1", "x5y1", "x6y1",
            "x7y1", "x8y1", "x9y1",
        ]
        with self.assertRaises(BoardException) as context:
            Unit(self.__board_mock, cell_keys_for_a_row, "block")
        self.assertTrue("Not a valid block" in str(context.exception))

    def test_init_valid_row_unit(self):
        cell_keys = [
            "x1y1", "x2y1", "x3y1",
            "x4y1", "x5y1", "x6y1",
            "x7y1", "x8y1", "x9y1",
        ]
        unit = Unit(self.__board_mock, cell_keys, "row")
        self.assertTrue(unit.is_row_unit())

    def test_init_invalid_row_unit(self):
        cell_keys_for_a_column = [
            "x1y1", "x1y2", "x1y2",
            "x1y4", "x1y5", "x1y6",
            "x1y7", "x1y8", "x1y9",
        ]
        with self.assertRaises(BoardException) as context:
            Unit(self.__board_mock, cell_keys_for_a_column, "row")
        self.assertTrue("Not a valid row; cell keys do not align" in str(context.exception))

    def test_init_valid_column_unit(self):
        cell_keys = [
            "x1y1", "x1y2", "x1y2",
            "x1y4", "x1y5", "x1y6",
            "x1y7", "x1y8", "x1y9",
        ]
        unit = Unit(self.__board_mock, cell_keys, "column")
        self.assertTrue(unit.is_column_unit())

    def test_init_invalid_colum_unit(self):
        cell_keys_for_a_row = [
            "x1y9", "x2y9", "x3y9",
            "x4y9", "x5y9", "x6y9",
            "x7y9", "x8y9", "x9y9",
        ]
        with self.assertRaises(BoardException) as context:
            Unit(self.__board_mock, cell_keys_for_a_row, "column")
        self.assertTrue("Not a valid column; cell keys do not align" in str(context.exception))

    def test_get_cell_keys(self):
        cell_keys = [
            "x1y9", "x2y9", "x3y9",
            "x4y9", "x5y9", "x6y9",
            "x7y9", "x8y9", "x9y9",
        ]
        unit = Unit(self.__board_mock, cell_keys, "row")
        self.assertEqual(unit.get_cell_keys(), cell_keys)

    def test_get_cells(self):
        # What we put in
        cell_keys = [
            "x1y9", "x2y9", "x3y9",
            "x4y9", "x5y9", "x6y9",
            "x7y9", "x8y9", "x9y9",
        ]
        # The result we want returned
        returned_cells = [
            Mock(), Mock(), Mock(),
            Mock(), Mock(), Mock(),
            Mock(), Mock(), Mock()
        ]
        # The args_list in the order in which we expect the get_cells method to be called
        expected_call_args_list = [
            call("x1y9",), call("x2y9",), call("x3y9",),
            call("x4y9",), call("x5y9",), call("x6y9", ),
            call("x7y9",), call("x8y9",), call("x9y9",),
        ]

        # Configure a Board mock who's method get_cells returns the list of cell mocks above
        board_mock = Mock()
        attrs = {'get_cell.side_effect': returned_cells}
        board_mock.configure_mock(**attrs)

        # Initialise the unit
        unit = Unit(board_mock, cell_keys, "row")

        # Execute & verify
        returned_cells = unit.get_cells()
        self.assertEqual(returned_cells, returned_cells)
        self.assertEqual(board_mock.get_cell.call_args_list, expected_call_args_list)


if __name__ == '__main__':
    unittest.main()
