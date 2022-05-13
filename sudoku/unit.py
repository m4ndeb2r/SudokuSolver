from exceptions import SudokuException


class Unit(object):
    def __init__(self, the_board, cell_keys, type):
        Unit.__validate_unit_keys(cell_keys)
        if type == "block":
            Unit.__validate_block_keys(cell_keys)
        elif type == "row":
            Unit.__validate_row_keys(cell_keys)
        elif type == "column":
            Unit.__validate_column_keys(cell_keys)
        else:
            raise SudokuException(f"Illegal unit type: '{type}'.")

        self.__board = the_board
        self.__cell_keys = cell_keys
        self.__type = type

    def is_block_unit(self):
        """Returns if the unit is a block unit."""
        return self.__type == "block"

    def is_row_unit(self):
        """Returns if the unit is a row unit."""
        return self.__type == "row"

    def is_column_unit(self):
        """Returns if the unit is a column unit."""
        return self.__type == "column"

    def get_cell_keys(self):
        """Returns the keys referring to the cells in the unit as a list."""
        return self.__cell_keys

    def get_cells(self):
        """Returns the cells in the unit as a list."""
        cells = []
        for key in self.__cell_keys:
            cells.append(self.__board.get_cell(key))
        if len(cells) != 9:
            raise SudokuException(f"Illegal number of cells in unit: {len(cells)}.")
        return cells

    def get_cell(self, key):
        """Returns the cell represented by the specified key, if present in this unit. If not
        present in the unit, None is returned."""
        if key in self.__cell_keys:
            return self.__board.get_cell(key)
        return None

    def get_horizontal_neighbours(self):
        """Returns the two block units at the left and/or right from the current block unit.
        If the current unit is not a block unit, an empty list is returned."""
        if not self.is_block_unit():
            return []
        horizontal_neighbours = []
        row_num_of_block_unit = self.__cell_keys[0][3:4]
        for unit in self.__board.get_block_units():
            if unit != self and unit.__cell_keys[0][3:4] == row_num_of_block_unit:
                horizontal_neighbours.append(unit)
        if len(horizontal_neighbours) != 2:
            raise SudokuException("Unexpected number of horizontal neighbour block units.")
        return horizontal_neighbours

    def get_vertical_neighbours(self):
        """Returns the two block units at on top and/or below the current block unit.
        If the current unit is not a block unit, an empty list is returned."""
        if not self.is_block_unit():
            return []
        vertical_neighbours = []
        col_num_of_block_unit = self.__cell_keys[0][1:2]
        for unit in self.__board.get_block_units():
            if unit != self and unit.__cell_keys[0][1:2] == col_num_of_block_unit:
                vertical_neighbours.append(unit)
        if len(vertical_neighbours) != 2:
            raise SudokuException("Unexpected number of vertical neighbour block units.")
        return vertical_neighbours

    def is_solved(self):
        """Determines if a unit is solved, e.g. all its cells are solved."""
        for cell in self.get_cells():
            if not cell.is_solved():
                return False
        return True

    def has_solved_cell_with_value(self, value):
        """Determines if a value within a unit is solved, e.g. the unit contains a
        cell that is solved with the specified value."""
        for cell in self.get_cells():
            if cell.is_solved() and cell.has_possible_value(value):
                return True
        return False

    def get_distinct_row_containing_possible_val(self, value):
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

    def validate(self):
        """Validates the unit. Checks for any illegal characters or illegal combinations."""
        solved_values = []
        for cell in self.get_cells():
            cell.validate()
            if cell.is_solved():
                solved_value = cell.get_solution()
                if solved_value in solved_values:
                    raise SudokuException(f"Value {solved_value} not unique in unit.")
                solved_values.append(solved_value)

    def __get_keys_of_cells_with_value(self, value):
        """Gathers all keys referring to cells containing the specified value as a possible value."""
        keys = []
        for key in self.get_cell_keys():
            if self.get_cell(key).has_possible_value(value):
                keys.append(key)
        return keys

    @staticmethod
    def __validate_unit_keys(cell_keys):
        if len(cell_keys) != 9:
            raise SudokuException(f"Not a valid unit: {cell_keys}.")
        valid_keys = []
        for x in range(1, 10):
            for y in range(1, 10):
                valid_keys.append(f"x{x}y{y}")
        for key in cell_keys:
            if key not in valid_keys:
                raise SudokuException(f"Not a valid unit; one or more keys not valid: {cell_keys}.")

    @staticmethod
    def __validate_block_keys(cell_keys):
        for i in [0, 3, 6]:
            row_keys = cell_keys[i: i + 3]
            try:
                Unit.__validate_row_keys(row_keys)
            except SudokuException:
                raise SudokuException(f"Not a valid block; cell keys in row do not align {row_keys}")
        for i in range(0, 3):
            column_keys = [cell_keys[i], cell_keys[i + 3], cell_keys[i + 6]]
            try:
                Unit.__validate_column_keys(column_keys)
            except SudokuException:
                raise SudokuException(f"Not a valid block; cell keys in column do not align {column_keys}")

    @staticmethod
    def __validate_row_keys(cell_keys):
        y = cell_keys[0][3:4]
        for key in cell_keys:
            if key[3:4] != y:
                raise SudokuException(f"Not a valid row; cell keys do not align: {cell_keys}.")

    @staticmethod
    def __validate_column_keys(cell_keys):
        x = cell_keys[0][1:2]
        for key in cell_keys:
            if key[1:2] != x:
                raise SudokuException(f"Not a valid column; cell keys do not align: {cell_keys}.")

