from board.block_unit import BlockUnit
from board.board_exception import BoardException
from board.cell import Cell
from board.column_unit import ColumnUnit
from board.row_unit import RowUnit


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
    # attempts.
    def solve(self):
        continue_solving = not self.is_solved()
        while continue_solving:
            updated = False
            for unit in self.__units:
                updated = unit.solve() or updated
            continue_solving = updated and not self.is_solved()
        self.validate()

    # Validates the board. Checks for any illegal characters or illegal combinations.
    def validate(self):
        for unit in self.__units:
            unit.validate()

    # Prints a board representation to the console.
    def print(self):
        for y in range(1, 10):
            for x in range(1, 10):
                print(self.__cells[f"x{x}y{y}"].to_string(), end='')
            print('')

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
