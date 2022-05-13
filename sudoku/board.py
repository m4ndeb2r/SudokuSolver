from unit import Unit
from cell import Cell
from single_unit_solver import SingleUnitSolver
from vertical_block_solver import VerticalBlockSolver
from horizontal_block_solver import HorizontalBlockSolver
from bidirectional_block_solver import BidirectionalBlockSolver
from exceptions import SudokuException


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

    def get_block_units(self):
        """Returns all block units on the board."""
        block_units = []
        for unit in self.__units:
            if unit.is_block_unit():
                block_units.append(unit)
        if len(block_units) != 9:
            raise SudokuException(f"Unexpected number of block units on the board: {len(block_units)}.")
        return block_units

    def get_cell(self, key):
        """Returns the cell with the specified key."""
        return self.__cells[key]

    def set_cell_value(self, key, value):
        """Sets a definitive value for the cell identified by the specified key."""
        self.__cells[key].set_value(value)

    def is_solved(self):
        """Determines if all the cells on the board are solved."""
        cells = list(self.__cells.values())
        for cell in cells:
            if not cell.is_solved():
                return False
        return True

    def solve(self):
        """Attempts to solve all the units (blocks, rows, columns) on the board.
        Solving will be repeated as long as one or more cells are solved by the
        attempts."""
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

    def validate(self):
        """Validates the board. Checks for any illegal characters or illegal combinations"""
        for unit in self.__units:
            unit.validate()

    def print(self):
        """Prints a board representation to the console."""
        for y in range(1, 10):
            for x in range(1, 10):
                print(self.__cells[f"x{x}y{y}"].to_string(), end='')
            print('')
