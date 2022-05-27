from board.abstract_unit import AbstractUnit
from board.board_exception import BoardException
from solver.single_unit_solver import SingleUnitSolver


# Respresents a row of 9 cells on a 9 x 9 sudoku board.
class RowUnit(AbstractUnit):
    def __init__(self, the_board, cell_keys):
        super().__init__(the_board, cell_keys)
        # Validate if the keys constitute a valid row
        RowUnit.__validate_row_keys(cell_keys)

    # Attempts to solve the row unit. Returns True if any of its cells was
    # changed, or False otherwise.
    def solve(self):
        return SingleUnitSolver.solve(self)

    # Validate if the keys constitute a valid row
    @staticmethod
    def __validate_row_keys(cell_keys):
        y = cell_keys[0][3:4]
        for key in cell_keys:
            if key[3:4] != y:
                raise BoardException(f"Not a valid row; cell keys do not align: {cell_keys}.")

