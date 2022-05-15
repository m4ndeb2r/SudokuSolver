from abc import ABC, abstractmethod
from board.board_exception import BoardException


# Abstract class Unit (inherits from ABC)
class AbstractUnit(ABC):
    def __init__(self, the_board, cell_keys):
        AbstractUnit.__validate_cell_keys(cell_keys)
        self.__board = the_board
        self.__cell_keys = cell_keys

    # Returns the board in which this unit sits.
    def get_board(self):
        return self.__board

    # Returns the keys referring to the cells in the unit as a list.
    def get_cell_keys(self):
        return self.__cell_keys

    # Returns the cells in the unit as a list.
    def get_cells(self):
        cells = []
        for key in self.__cell_keys:
            cells.append(self.__board.get_cell(key))
        if len(cells) != 9:
            raise BoardException(f"Illegal number of cells in unit: {len(cells)}.")
        return cells

    # Returns the cell represented by the specified key, if present in this unit.
    # If not present in the unit, None is returned.
    def get_cell(self, key):
        if key in self.__cell_keys:
            return self.__board.get_cell(key)
        return None

    # Attempts to solve the unit
    @abstractmethod
    def solve(self):
        pass

    # Determines if a unit is solved, e.g. all its cells are solved.
    def is_solved(self):
        for cell in self.get_cells():
            if not cell.is_solved():
                return False
        return True

    # Determines if a value within a unit is solved, e.g. the unit contains a
    # cell that is solved with the specified value.
    def has_solved_cell_with_value(self, value):
        for cell in self.get_cells():
            if cell.is_solved() and cell.has_possible_value(value):
                return True
        return False

    # Validates the unit. Checks for any illegal characters or illegal combinations.
    def validate(self):
        solved_values = []
        for cell in self.get_cells():
            cell.validate()
            if cell.is_solved():
                solved_value = cell.get_solution()
                if solved_value in solved_values:
                    raise BoardException(f"Value {solved_value} not unique in unit.")
                solved_values.append(solved_value)

    @staticmethod
    def __validate_cell_keys(cell_keys):
        if len(cell_keys) != 9:
            raise BoardException(f"Not a valid unit: {cell_keys}.")
        valid_keys = []
        for x in range(1, 10):
            for y in range(1, 10):
                valid_keys.append(f"x{x}y{y}")
        for key in cell_keys:
            if key not in valid_keys:
                raise BoardException(f"Not a valid unit; one or more keys not valid: {cell_keys}.")
