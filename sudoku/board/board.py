from board.board_exception import BoardException
from solver.bidirectional_block_solver import BidirectionalBlockSolver
from solver.horizontal_block_solver import HorizontalBlockSolver
from solver.single_unit_solver import SingleUnitSolver
from solver.vertical_block_solver import VerticalBlockSolver
from board.unit import Unit
from board.cell import Cell


class Board(object):

    def __init__(self):
        # Initialise cells
        self.__cells = {}
        for y in range(1, 10):
            for x in range(1, 10):
                self.__cells[f"x{x}y{y}"] = Cell()

        # Initialise units (rows, columns and blocks)
        self.__units = []

        # Units: rows
        for y in range(1, 10):
            cell_keys = []
            for x in range(1, 10):
                cell_keys.append(f"x{x}y{y}")
            self.__units.append(Unit(self, cell_keys, "row"))

        # Units: columns
        for x in range(1, 10):
            cell_keys = []
            for y in range(1, 10):
                cell_keys.append(f"x{x}y{y}")
            self.__units.append(Unit(self, cell_keys, "column"))

        # Units: blocks 3 x 3
        y = 1
        while y < 10:
            x = 1
            while x < 10:
                cell_keys = []
                for _y in range(y, y + 3):
                    for _x in range(x, x + 3):
                        cell_keys.append(f"x{_x}y{_y}")
                self.__units.append(Unit(self, cell_keys, "block"))
                x += 3
            y += 3

    # Returns all block units on the board.
    def get_block_units(self):
        block_units = []
        for unit in self.__units:
            if unit.is_block_unit():
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
                updated = SingleUnitSolver.solve(unit) or updated
            for unit in self.__units:
                if unit.is_block_unit():
                    updated = HorizontalBlockSolver.solve(unit) or updated
                    updated = SingleUnitSolver.solve(unit) or updated
            for unit in self.__units:
                if unit.is_block_unit():
                    updated = VerticalBlockSolver.solve(unit) or updated
                    updated = SingleUnitSolver.solve(unit) or updated
            for unit in self.__units:
                if unit.is_block_unit():
                    updated = BidirectionalBlockSolver.solve(unit) or updated
                    updated = SingleUnitSolver.solve(unit) or updated
            continue_solving = updated and not self.is_solved()

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
