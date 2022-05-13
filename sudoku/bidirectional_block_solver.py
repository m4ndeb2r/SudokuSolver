from exceptions import SudokuException


class BidirectionalBlockSolver(object):

    # Attempts to solve the specified unit by comparing it to its horizontal and vertical
    # neighbour block units. Returns True if any cell was changed, or False otherwise.
    @staticmethod
    def solve(unit):
        updated = False
        if not unit.is_block_unit():
            return updated
        if unit.is_solved():
            return updated

        # Get block units left and right from the current block unit
        horizontal_neighbours = unit.get_horizontal_neighbours()
        # Get block units above and below the current block unit
        vertical_neighbours = unit.get_vertical_neighbours()

        for value in range(1, 10):
            # If the unit contains a solved cell with the current value, continue to the next value.
            if unit.has_solved_cell_with_value(value):
                continue

            r1_pos = horizontal_neighbours[0].get_distinct_row_containing_possible_val(value)
            r2_pos = horizontal_neighbours[1].get_distinct_row_containing_possible_val(value)
            c1_pos = vertical_neighbours[0].get_distinct_column_containing_possible_val(value)
            c2_pos = vertical_neighbours[1].get_distinct_column_containing_possible_val(value)

            # Determine the index of the cell we can solve, based on the info above.
            # Using list comprehension to which position is not in [r1_pos, r2_pos]
            # (or [c1_pos, c2_pos])
            r_pos = [x for x in [0, 1, 2] if x not in [r1_pos, r2_pos]]
            c_pos = [x for x in [0, 1, 2] if x not in [c1_pos, c2_pos]]

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
                raise SudokuException("Unexpected program error: attempting to solve a previously solved cell.")
            unit.get_cells()[idx].set_value(value)
            updated = True

        return updated
