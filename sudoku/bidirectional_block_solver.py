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
            # If the unit contains a solved cell with the current value, continue to the next value.
            if unit.has_solved_cell_with_value(value):
                continue

            r1_pos = BidirectionalBlockSolver.__get_distinct_row_containing_possible_val(horizontal_neighbours[0], value)
            r2_pos = BidirectionalBlockSolver.__get_distinct_row_containing_possible_val(horizontal_neighbours[1], value)
            c1_pos = BidirectionalBlockSolver.__get_distinct_column_containing_possible_val(vertical_neighbours[0], value)
            c2_pos = BidirectionalBlockSolver.__get_distinct_column_containing_possible_val(vertical_neighbours[1], value)

            # Determine the index of the cell we can solve, based on the info above.
            r_pos = BidirectionalBlockSolver.__get_solvable_pos(r1_pos, r2_pos)
            c_pos = BidirectionalBlockSolver.__get_solvable_pos(c1_pos, c2_pos)

            # See if some finetuning is necessary: if we do not have a distinct row (r_pos
            # contains > 1 element) and a distinct col (c_pos contains > 1 element), we might
            # be able to tidy things up when r_pos and c_pos refer to cells that have already
            # been solved in the current block unit.
            if len(r_pos) != 1 or len(c_pos) != 1:
                # Let's finetune r_pos and/or c_pos ...
                # First, we need copies of r_pos and c_pos to prevent concurrent modification
                # errors below.
                r_pos_copy = []
                for r in r_pos:
                    r_pos_copy.append(r)
                c_pos_copy = []
                for c in c_pos:
                    c_pos_copy.append(c)

                # If all cells in a block row represented by r_pos and c_pos are solved,
                # remove the row position from r_pos.
                for r in r_pos_copy:
                    all_in_block_row_solved = True
                    for c in c_pos_copy:
                        idx = 3 * r + c
                        if not unit.get_cells()[idx].is_solved():
                            all_in_block_row_solved = False
                    if all_in_block_row_solved:
                        r_pos.remove(r)

                # If all cells in a block column represented by r_pos and c_pos are solved,
                # remove the column position from c_pos.
                for c in c_pos_copy:
                    all_in_block_col_solved = True
                    for r in r_pos_copy:
                        idx = 3 * r + c
                        if not unit.get_cells()[idx].is_solved():
                            all_in_block_col_solved = False
                    if all_in_block_col_solved:
                        c_pos.remove(c)

            # If we have a distinct row and a distinct column, we can determine the index of the
            # solvable cell. If not, continue to the next value.
            if len(r_pos) != 1 or len(c_pos) != 1:
                continue
            idx = 3 * r_pos[0] + c_pos[0]

            # Solve the cell on index idx (and raise an error if that cell was previously solved;
            # this should NEVER be the case).
            if unit.get_cells()[idx].is_solved():
                raise Exception("Unexpected program error: attempting to solve a previously solved cell.")
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
    def __get_distinct_row_containing_possible_val(unit, value):
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
    def __get_distinct_column_containing_possible_val(unit, value):
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

