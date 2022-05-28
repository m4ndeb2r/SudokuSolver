from solver.solver_exception import SolverException
from sudoku_exception import SudokuException


class BruteForceBoardSolver(object):

    # Attempts to solve the specified board by brute force. Returns the resulting board.
    @staticmethod
    def solve(board):
        if board.is_solved():
            return board

        # The board is initially valid
        # We work with a clone so we don't disturb the initial board
        cloned_board = board.clone()
        # We're trying every possible value in the first unsolved cell we encounter
        first_unsolved_cell = cloned_board.get_first_unsolved_cell()
        wild_guesses = first_unsolved_cell.get_possible_values()[:]
        for wild_guess in wild_guesses:
            # Our attempt may invalidate the board (Exception)
            # In that case, move on to the next 'wild guess'
            try:
                first_unsolved_cell.set_value(wild_guess)
                result = cloned_board.solve()
                if result.is_solved():
                    return result
            except SudokuException:
                continue

        return board
