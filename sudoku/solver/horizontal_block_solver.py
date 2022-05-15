class HorizontalBlockSolver(object):

    # Attempts to solve the specified unit by comparing it to its horizontal neighbour
    # block units. Returns True if any cell was changed, or False otherwise.
    @staticmethod
    def solve(unit):
        updated = False
        if unit.is_solved():
            return updated

        # Get block units left and right from teh current block unit
        horizontal_neighbours = unit.get_horizontal_neighbours()

        for value in range(1, 10):
            # If the unit contains a solved cell with the current value, continue to the next value.
            if unit.has_solved_cell_with_value(value):
                continue

            for n in range(0, 2):
                rn_pos = horizontal_neighbours[n].get_distinct_row_containing_possible_val(value)
                if rn_pos is not None:
                    for i in range(rn_pos * 3, rn_pos * 3 + 3):
                        cell = unit.get_cells()[i]
                        if cell.has_possible_value(value):
                            cell.remove_possible_value(value)
                            updated = True

        return updated
