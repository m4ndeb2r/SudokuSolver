from unit import Unit
from cell import Cell
from single_unit_solver import SingleUnitSolver
from bidirectional_block_solver import BidirectionalBlockSolver


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
            raise Exception(f"Unexpected number of block units on the board: {len(block_units)}.")
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
        continue_solving = True
        while not self.is_solved() and continue_solving:
            continue_solving = False
            for unit in self.__units:
                continue_solving = SingleUnitSolver.solve(unit) or continue_solving
            for unit in self.__units:
                if unit.is_block_unit():
                    continue_solving = BidirectionalBlockSolver.solve(unit) or continue_solving
                    continue_solving = SingleUnitSolver.solve(unit) or continue_solving

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
