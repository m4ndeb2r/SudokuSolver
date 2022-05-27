from board.block_unit import BlockUnit
from board.board_exception import BoardException
from board.cell import Cell
from board.column_unit import ColumnUnit
from board.row_unit import RowUnit
from solver.brute_force_board_solver import BruteForceBoardSolver


class Board(object):

    # Constructor accepting a list of nine rows, each consisting of 9 characters
    # in the set ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9'], where '.'
    # represents an unsolved cell, and any digit represents a solved cell.
    # The input parameter is optional: when left empty, all cells will be unsolved.
    def __init__(self, rows):
        # Initialise cells
        self.__cells = {}
        for y in range(1, 10):
            for x in range(1, 10):
                self.__cells[f"x{x}y{y}"] = Cell()

        # Initialise units (rows, columns and blocks)
        self.__units = []
        self.__create_row_units()
        self.__create_column_units()
        self.__create_block_units()

        # Fill in the solved cells, based on the input parameter rows.
        if rows:
            if len(rows) != 9:
                raise BoardException(f"Illegal number of rows: '{len(rows)}'. Nr. of rows must be 9.")
            for y in range(0, 9):
                row = rows[y]
                if len(row) != 9:
                    raise BoardException(f"Illegal number of cells in row: '{len(row)}'. Nr. of cells must be 9.")
                row_values = list(row)
                for x in range(0, 9):
                    value = row_values[x]
                    if value not in ('.', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        raise BoardException(f"Illegal value for cell: '{value}'. "
                                             "Only digits [1-9] or '.' (empty cell) are allowed.")
                    if value != '.':
                        self.set_cell_value(f"x{x + 1}y{y + 1}", value)
                        self.validate()

    # Returns all block units on the board.
    def get_block_units(self):
        block_units = []
        for unit in self.__units:
            if isinstance(unit, BlockUnit):
                block_units.append(unit)
        if len(block_units) != 9:
            raise BoardException(f"Unexpected number of block units on the board: {len(block_units)}.")
        return block_units

    # Returns the cell with the specified key.
    def get_cell(self, key):
        return self.__cells[key]

    # Returns the first cell that is yet unsolved, or None if all the cells are solved.
    def get_first_unsolved_cell(self):
        for cell in self.__cells.values():
            if not cell.is_solved():
                return cell
        return None

    # Sets a definitive value for the cell identified by the specified key.
    def set_cell_value(self, key, value):
        self.__cells[key].set_value(value)

    # Determines if all the cells on the board are solved.
    def is_solved(self):
        cells = list(self.__cells.values())
        for cell in cells:
            if not cell.is_solved():
                return False
        return True

    # Attempts to solve all the units (blocks, rows, columns) on the board.
    # Solving will be repeated as long as one or more cells are solved by the
    # attempts. If units are no longer able to solve themselves, a brute force
    # board solver will make a recursive attempt to solve the board.
    # Returns the updated/solved board.
    # Raises a SudokuException if the board becomes invalid
    def solve(self):
        # Solve units separtely
        continue_solving_units = not self.is_solved()
        while continue_solving_units:
            updated = False
            for unit in self.__units:
                updated = unit.solve() or updated
            continue_solving_units = updated and not self.is_solved()
        self.validate()
        # Solve the (rest of the) board by brute force
        return BruteForceBoardSolver.solve(self)

    # Validates the board. Checks for any illegal characters or illegal combinations.
    def validate(self):
        for unit in self.__units:
            unit.validate()

    # Returns a string representation of the board.
    def to_string(self):
        string = ""
        for y in range(1, 10):
            for x in range(1, 10):
                string += self.__cells[f"x{x}y{y}"].to_string()
            if y < 9:
                string += "\n"
        return string

    # Returns a clone (deep copy) of this board.
    def clone(self):
        rows = ['.........' for x in range(9)]
        all_possible_values = [x for x in range(1, 10)]
        clone = Board(rows)
        for y in range(1, 10):
            for x in range(1, 10):
                key = f'x{x}y{y}'
                current_cell_possible_values = self.__cells[key].get_possible_values()
                removables = [x for x in all_possible_values if x not in current_cell_possible_values]
                clone.__cells[key].remove_possible_values(removables)
        clone.validate()
        return clone

    # Returns whether two boards are equal (all cells have the same possible values)
    def equals(self, other):
        for y in range(1, 10):
            for x in range(1, 10):
                self_pos_vals = self.get_cell(f'x{x}y{y}').get_possible_values()
                other_pos_vals = other.get_cell(f'x{x}y{y}').get_possible_values()
                if len(self_pos_vals) != len(other_pos_vals):
                    return False
                for i in range(0, len(self_pos_vals)):
                    if self_pos_vals[i] != other_pos_vals[i]:
                        return False
        return True

    # Prints a board representation to the console.
    def print(self):
        print(self.to_string())

    # Prints several boards to the console, next to each other.
    # TODO ... For future use (enable the user to pick a preset from one of the boards ...
    @staticmethod
    def print_multiple_boards(boards):
        for y in range(1, 10):
            for x in range(1, 10):
                for board in boards:
                    print(board.__cells[f"x{x}y{y}"].to_string(), end='')
            print('    ')

    # Creates all block units on the board.
    def __create_block_units(self):
        y = 1
        while y < 10:
            x = 1
            while x < 10:
                cell_keys = []
                for _y in range(y, y + 3):
                    for _x in range(x, x + 3):
                        cell_keys.append(f"x{_x}y{_y}")
                self.__units.append(BlockUnit(self, cell_keys))
                x += 3
            y += 3

    # Creates all row units on the board.
    def __create_row_units(self):
        for y in range(1, 10):
            cell_keys = []
            for x in range(1, 10):
                cell_keys.append(f"x{x}y{y}")
            self.__units.append(RowUnit(self, cell_keys))

    # Creates all column units on the board.
    def __create_column_units(self):
        for x in range(1, 10):
            cell_keys = []
            for y in range(1, 10):
                cell_keys.append(f"x{x}y{y}")
            self.__units.append(ColumnUnit(self, cell_keys))
