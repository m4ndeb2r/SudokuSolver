import unittest

from board.board import Board
from board.board_exception import BoardException


class TestBoard(unittest.TestCase):

    def test_init_invalid_nr_of_rows(self):
        invalid_rows = [
            '.........',
            '.........'
        ]
        with self.assertRaises(BoardException) as context:
            Board(invalid_rows)
        self.assertTrue("Illegal number of rows: '2'. Nr. of rows must be 9." in str(context.exception))

    def test_init_invalid_nr_of_cells_in_row(self):
        invalid_rows = [
            '.........',
            '........',
            '.........',
            '.........',
            '.........',
            '.........',
            '.........',
            '.........',
            '.........'
        ]
        with self.assertRaises(BoardException) as context:
            Board(invalid_rows)
        self.assertTrue("Illegal number of cells in row: '8'. Nr. of cells must be 9." in str(context.exception))

    def test_init_invalid_value_in_cell(self):
        invalid_rows = [
            '..1......',
            '........a',
            '...23....',
            '.....45..',
            '.......67',
            '.........',
            '.........',
            '.........',
            '.........'
        ]
        with self.assertRaises(BoardException) as context:
            Board(invalid_rows)
        self.assertTrue("Illegal value for cell: 'a'. Only digits [1-9] or '.' (empty cell) are allowed."
                        in str(context.exception))

    def test_init_valid_rows(self):
        valid_rows = [
            '.57....68',
            '683......',
            '1..896...',
            '..846..9.',
            '74.9..35.',
            '3...17.46',
            '4...5..8.',
            '2.918.573',
            '.35.72...'
        ]
        # No exception expected
        board = Board(valid_rows)
        # Test a few cells:
        self.assertEqual(board.get_cell("x1y1").get_possible_values(), [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(board.get_cell("x2y1").get_possible_values(), [5])
        self.assertEqual(board.get_cell("x3y1").get_possible_values(), [7])

    def test_clone(self):
        # Prepare: create an original board and solve partly
        rows = [
            '.57....68',
            '683......',
            '1..896...',
            '..846..9.',
            '74.9..35.',
            '3...17.46',
            '4...5..8.',
            '2.918.573',
            '.35.72...'
        ]
        original_board = Board(rows)
        for unit in original_board.get_block_units():
            unit.solve()
        # Execute:clone the original board
        cloned_board = original_board.clone()
        # Verify: check the clone
        self.assertIsNot(original_board, cloned_board)
        for y in range(1, 10):
            for x in range(1, 10):
                self.assertEqual(
                    original_board.get_cell(f"x{x}y{y}").get_possible_values(),
                    cloned_board.get_cell(f"x{x}y{y}").get_possible_values()
                )

    def test_equals(self):
        # Prepare: create an original board and solve partly
        rows = [
            '.57....68',
            '683......',
            '1..896...',
            '..846..9.',
            '74.9..35.',
            '3...17.46',
            '4...5..8.',
            '2.918.573',
            '.35.72...'
        ]
        original_board = Board(rows)
        cloned_board = original_board.clone()
        # Verify: test the equals method
        self.assertTrue(original_board.equals(cloned_board))
        cloned_board.set_cell_value("x1y1", 9)
        self.assertFalse(original_board.equals(cloned_board))

    def test_get_first_unsolved_cell(self):
        rows = [
            '.57....68',
            '683......',
            '1..896...',
            '..846..9.',
            '74.9..35.',
            '3...17.46',
            '4...5..8.',
            '2.918.573',
            '.35.72...'
        ]
        board = Board(rows)
        self.assertIs(board.get_first_unsolved_cell(), board.get_cell("x1y1"))

        rows = [
            '57.....68',
            '683......',
            '1..896...',
            '..846..9.',
            '74.9..35.',
            '3...17.46',
            '4...5..8.',
            '2.918.573',
            '.35.72...'
        ]
        board = Board(rows)
        self.assertIs(board.get_first_unsolved_cell(), board.get_cell("x3y1"))

        rows = [
            '243895716',
            '597316842',
            '618247359',
            '135672984',
            '764189523',
            '982453167',
            '356728491',
            '479561238',
            '821934675'
        ]
        board = Board(rows)
        self.assertEqual(board.get_first_unsolved_cell(), None)

    def test_solve(self):
        # Create a board
        initial_board = [
            '....9..16',
            '..7..6.42',
            '..8..7...',
            '135...9..',
            '...18.5..',
            '........7',
            '3567....1',
            '..9....3.',
            '8...3....'
        ]
        board = Board(initial_board)

        # Solve it
        board.solve()

        # Test the solution:
        self.assertTrue(board.is_solved())
        self.assertEqual(
            board.to_string(),
            " 2  4  3  8  9  5  7  1  6 \n"
            " 5  9  7  3  1  6  8  4  2 \n"
            " 6  1  8  2  4  7  3  5  9 \n"
            " 1  3  5  6  7  2  9  8  4 \n"
            " 7  6  4  1  8  9  5  2  3 \n"
            " 9  8  2  4  5  3  1  6  7 \n"
            " 3  5  6  7  2  8  4  9  1 \n"
            " 4  7  9  5  6  1  2  3  8 \n"
            " 8  2  1  9  3  4  6  7  5 "
        )


if __name__ == '__main__':
    unittest.main()
