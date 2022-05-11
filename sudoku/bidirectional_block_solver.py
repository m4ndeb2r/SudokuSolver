class BidirectionalBlockSolver(object):

    @staticmethod
    def solve(unit):
        """Attempts to solve the specified unit by comparing it to its horizontal and vertical neighbour block units.
        Returns True if any cell was changed, or False otherwise."""
        updated = False
        if not unit.is_block_unit():
            return updated
        if unit.is_solved():
            return updated

        horizontal_neighbours = unit.get_horizontal_neighbours()
        vertical_neighbours = unit.get_vertical_neighbours()

        for value in range(1, 10):
            h1_pos = BidirectionalBlockSolver.__get_unique_row_containing_possible_value(horizontal_neighbours[0], value)
            h2_pos = BidirectionalBlockSolver.__get_unique_row_containing_possible_value(horizontal_neighbours[1], value)
            v1_pos = BidirectionalBlockSolver.__get_unique_column_containing_possible_value(vertical_neighbours[0], value)
            v2_pos = BidirectionalBlockSolver.__get_unique_column_containing_possible_value(vertical_neighbours[1], value)

            # Determine the index of the cell we can solve, based on the info above
            h_pos = BidirectionalBlockSolver.__get_solvable_pos(h1_pos, h2_pos)
            if len(h_pos) != 1:
                continue
            v_pos = BidirectionalBlockSolver.__get_solvable_pos(v1_pos, v2_pos)
            if len(v_pos) != 1:
                continue
            idx = 3 * h_pos[0] + v_pos[0]

            # Solve the cell on index idx
            if not unit.get_cells()[idx].is_solved():
                unit.get_cells()[idx].set_value(value)
                updated = True

        return updated

    @staticmethod
    def __get_solvable_pos(v1_pos, v2_pos):
        v_pos = [0, 1, 2]
        if v1_pos is not None and v1_pos in v_pos:
            v_pos.remove(v1_pos)
        if v2_pos is not None and v2_pos in v_pos:
            v_pos.remove(v2_pos)
        return v_pos

    @staticmethod
    def __get_unique_row_containing_possible_value(unit, value):
        keys = BidirectionalBlockSolver.__get_keys_of_cells_with_value(unit, value)
        # Not found? Return None
        if len(keys) == 0:
            return None
        # Found? Are they on the same row (based on the key)?
        # Then the row index within the unit is returned, or None otherwise
        for i in range(0, len(keys)):
            if keys[i][2:4] != keys[0][2:4]:
                return None
        return (int(keys[0][3:4]) - 1) % 3

    @staticmethod
    def __get_unique_column_containing_possible_value(unit, value):
        keys = BidirectionalBlockSolver.__get_keys_of_cells_with_value(unit, value)
        # Not found? Return None
        if len(keys) == 0:
            return False
        # Found? Are they on the same row (based on the key)?
        # Then the column index within the unit is returned, or None otherwise
        for i in range(0, len(keys)):
            if keys[i][0:2] != keys[0][0:2]:
                return None
        return (int(keys[0][1:2]) - 1) % 3

    @staticmethod
    def __get_keys_of_cells_with_value(unit, value):
        """Gathers all keys referring to cells containing the specified value as a possible value."""
        keys = []
        for key in unit.get_cell_keys():
            if unit.get_cell(key).has_possible_value(value):
                keys.append(key)
        return keys

