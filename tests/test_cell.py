import unittest

from cell import Cell
from exceptions import SudokuException


class TestCell(unittest.TestCase):

    def setUp(self):
        self.cell = Cell()

    def test_init(self):
        for i in range(1, 10):
            self.assertTrue(self.cell.has_possible_value(i), f"Valid possible value {i} expected but not present.")
        self.assertFalse(self.cell.has_possible_value(0), f"Illegal possible value: {0}.")
        self.assertFalse(self.cell.has_possible_value(10), f"Illegal possible value: {10}.")
        self.assertFalse(self.cell.is_solved(), "Expected cell NOT to be solved.")
        try:
            self.cell.validate()
        except SudokuException:
            self.fail("Expected cell to be valid after initialisation.")

    def test_solve_by_set_value(self):
        self.assertFalse(self.cell.is_solved(), "Expected cell NOT to be solved.")
        self.cell.set_value(1)
        self.assertTrue(self.cell.is_solved(), "Expected cell NOT to be solved.")

    def test_set_value_exception(self):
        with self.assertRaises(SudokuException):
            self.cell.set_value(0)
        with self.assertRaises(SudokuException):
            self.cell.set_value('10')
        with self.assertRaises(ValueError):
            self.cell.set_value('a')

    def test_solve_by_removing_possible_value(self):
        self.assertFalse(self.cell.is_solved(), "Expected cell NOT to be solved.")
        for i in range(1, 9):
            self.cell.remove_possible_value(i)
        self.assertTrue(self.cell.is_solved(), "Expected cell to be solved.")
        with self.assertRaises(SudokuException):
            self.cell.remove_possible_value(9)

    def test_solve_by_removing_possible_values(self):
        self.assertFalse(self.cell.is_solved())
        self.cell.remove_possible_values([1, 2, 3, 4, 5, 6])
        self.assertFalse(self.cell.is_solved(), "Expected cell NOT to be solved.")
        self.cell.remove_possible_values([7, 8])
        self.assertTrue(self.cell.is_solved(), "Expected cell to be solved.")
        with self.assertRaises(SudokuException):
            self.cell.remove_possible_values([9])

    def test_get_solution(self):
        self.assertIsNone(self.cell.get_solution(), "Expected solution to be 'None'.")
        self.cell.set_value(6)
        self.assertEqual(self.cell.get_solution(), 6, "Expected solution to be 6 (numerical).")

    def test_to_string(self):
        self.assertEqual(self.cell.to_string(), " . ")
        self.cell.set_value(5)
        self.assertEqual(self.cell.to_string(), " 5 ")


if __name__ == '__main__':
    unittest.main()