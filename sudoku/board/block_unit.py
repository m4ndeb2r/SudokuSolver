from board.abstract_unit import AbstractUnit
from board.board_exception import BoardException
from solver.bidirectional_block_solver import BidirectionalBlockSolver
from solver.horizontal_block_solver import HorizontalBlockSolver
from solver.single_unit_solver import SingleUnitSolver
from solver.vertical_block_solver import VerticalBlockSolver


# Respresents a 3 x 3 block of cells on a 9 x 9 sudoku board.
class BlockUnit(AbstractUnit):
    # An ordered sequence of solvers, used by the solve method
    # in the same order to solve this block unit
    SOLVER_SEQUENCE = [
        SingleUnitSolver,
        HorizontalBlockSolver,
        SingleUnitSolver,
        VerticalBlockSolver,
        SingleUnitSolver,
        BidirectionalBlockSolver,
        SingleUnitSolver
    ]

    def __init__(self, the_board, cell_keys):
        super().__init__(the_board, cell_keys)

        # Validate if the keys constitute a valid block
        BlockUnit.__validate_block_keys(cell_keys)

    # Attempts to solve the block unit. Returns True if any of its cells was
    # changed, or False otherwise.
    def solve(self):
        updated = False
        for solver in BlockUnit.SOLVER_SEQUENCE:
            if self.is_solved():
                return updated
            updated = solver.solve(self)
        return updated

    # Returns the two block units at the left and/or right from the current block unit.
    # If the current unit is not a block unit, an empty list is returned.
    def get_horizontal_neighbours(self):
        horizontal_neighbours = []
        row_num_of_block_unit = self.get_cell_keys()[0][3:4]
        for block_unit in self.get_board().get_block_units():
            if block_unit != self and block_unit.get_cell_keys()[0][3:4] == row_num_of_block_unit:
                horizontal_neighbours.append(block_unit)
        if len(horizontal_neighbours) != 2:
            raise BoardException("Unexpected number of horizontal neighbour block units.")
        return horizontal_neighbours

    # Returns the two block units at on top and/or below the current block unit.
    # If the current unit is not a block unit, an empty list is returned.
    def get_vertical_neighbours(self):
        vertical_neighbours = []
        col_num_of_block_unit = self.get_cell_keys()[0][1:2]
        for block_unit in self.get_board().get_block_units():
            if block_unit != self and block_unit.get_cell_keys()[0][1:2] == col_num_of_block_unit:
                vertical_neighbours.append(block_unit)
        if len(vertical_neighbours) != 2:
            raise BoardException("Unexpected number of vertical neighbour block units.")
        return vertical_neighbours

    def get_distinct_row_containing_possible_val(self, value):
        # Get the keys of all cells in the unit that have the specified possible value
        keys = self.__get_keys_of_cells_with_value(value)
        # Not found? Return None
        if len(keys) == 0:
            return None
        # Found? Are they on the same row (based on the key)?
        # Then the row index within the unit is returned, or None otherwise
        for i in range(0, len(keys)):
            if keys[i][2:4] != keys[0][2:4]:
                return None
        return (int(keys[0][3:4]) - 1) % 3

    def get_distinct_column_containing_possible_val(self, value):
        # Get the keys of all cells in the unit that have the specified possible value
        keys = self.__get_keys_of_cells_with_value(value)
        # Not found? Return None
        if len(keys) == 0:
            return None
        # Found? Are they on the same row (based on the key)?
        # Then the column index within the unit is returned, or None otherwise
        for i in range(0, len(keys)):
            if keys[i][0:2] != keys[0][0:2]:
                return None
        return (int(keys[0][1:2]) - 1) % 3

    # Gathers all keys referring to cells containing the specified value as a possible value.
    def __get_keys_of_cells_with_value(self, value):
        keys = []
        for key in self.get_cell_keys():
            if self.get_cell(key).has_possible_value(value):
                keys.append(key)
        return keys

    # Validate if the keys constitute a valid block
    @staticmethod
    def __validate_block_keys(cell_keys):
        for i in [0, 3, 6]:
            row_keys = cell_keys[i: i + 3]
            y = row_keys[0][3:4]
            for key in row_keys:
                if key[3:4] != y:
                    raise BoardException(f"Not a valid block; cell keys in row do not align {row_keys}")
        for i in range(0, 3):
            column_keys = [cell_keys[i], cell_keys[i + 3], cell_keys[i + 6]]
            x = column_keys[0][1:2]
            for key in column_keys:
                if key[1:2] != x:
                    raise BoardException(f"Not a valid block; cell keys in column do not align {column_keys}")
