from board.abstract_unit import AbstractUnit
from board.board_exception import BoardException
from solver.single_unit_solver import SingleUnitSolver


# Respresents a column of 9 cells on a 9 x 9 sudoku board.
class ColumnUnit(AbstractUnit):
    def __init__(self, the_board, cell_keys):
        super().__init__(the_board, cell_keys)
        # Validate if the keys constitute a valid column
        ColumnUnit.__validate_column_keys(cell_keys)

    # Attempts to solve the row unit
    def solve(self):
        return SingleUnitSolver.solve(self)

    # Validate if the keys constitute a valid column
    @staticmethod
    def __validate_column_keys(cell_keys):
        x = cell_keys[0][1:2]
        for key in cell_keys:
            if key[1:2] != x:
                raise BoardException(f"Not a valid column; cell keys do not align: {cell_keys}.")

