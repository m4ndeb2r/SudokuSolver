import unittest
from unittest.mock import Mock, call

from board.board_exception import BoardException
from board.column_unit import ColumnUnit
from board.row_unit import RowUnit


class TestAbstractUnit(unittest.TestCase):

    __board_mock = Mock()

    def test_init_invalid_nr_of_cell_keys(self):
        with self.assertRaises(BoardException) as context:
            RowUnit(self.__board_mock, ["x1y7", "x1y8", "x1y9"])
        self.assertTrue("Not a valid unit: ['x1y7', 'x1y8', 'x1y9']." in str(context.exception))

    def test_init_invalid_cell_keys(self):
        invalid_cell_keys = [
            "x0y1", "x0y1", "x0y1",
            "x0y2", "x0y2", "x0y2",
            "x0y3", "x0y3", "x0y3",
        ]
        with self.assertRaises(BoardException) as context:
            ColumnUnit(self.__board_mock, invalid_cell_keys)
        self.assertTrue("Not a valid unit; one or more keys not valid: " in str(context.exception))

    def test_get_cell_keys(self):
        cell_keys = [
            "x1y9", "x2y9", "x3y9",
            "x4y9", "x5y9", "x6y9",
            "x7y9", "x8y9", "x9y9",
        ]
        unit = RowUnit(self.__board_mock, cell_keys)
        self.assertEqual(unit.get_cell_keys(), cell_keys)

    def test_get_cells(self):
        # What we put in
        cell_keys = [
            "x1y9", "x2y9", "x3y9",
            "x4y9", "x5y9", "x6y9",
            "x7y9", "x8y9", "x9y9",
        ]
        # The result we want returned
        expected_returned_cells = [
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
        attrs = {'get_cell.side_effect': expected_returned_cells}
        board_mock.configure_mock(**attrs)

        # Initialise the unit
        unit = RowUnit(board_mock, cell_keys)

        # Execute & verify
        returned_cells = unit.get_cells()
        self.assertEqual(returned_cells, expected_returned_cells)
        self.assertEqual(board_mock.get_cell.call_args_list, expected_call_args_list)

    def test_get_cell(self):
        # What we put in
        cell_keys = [
            "x1y9", "x2y9", "x3y9",
            "x4y9", "x5y9", "x6y9",
            "x7y9", "x8y9", "x9y9",
        ]
        # The result we want returned
        expected_returned_cell = Mock()
        # The args_list in the order in which we expect the get_cells method to be called
        expected_call_args = call("x9y9",)

        # Configure a Board mock who's method get_cells returns the list of cell mocks above
        board_mock = Mock()
        attrs = {'get_cell.return_value': expected_returned_cell}
        board_mock.configure_mock(**attrs)

        # Initialise the unit
        unit = RowUnit(board_mock, cell_keys)

        # Execute & verify
        returned_cell = unit.get_cell("x9y9")
        self.assertEqual(returned_cell, expected_returned_cell)
        self.assertEqual(board_mock.get_cell.call_args, expected_call_args)


if __name__ == '__main__':
    unittest.main()
