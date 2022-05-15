class VerticalBlockSolver(object):

    # Attempts to solve the specified unit by comparing it to its vertical neighbour
    # block units. Returns True if any cell was changed, or False otherwise.
    @staticmethod
    def solve(unit):
        updated = False
        if unit.is_solved():
            return updated

        # Get block units above and below the current block unit
        vertical_neighbours = unit.get_vertical_neighbours()

        for value in range(1, 10):
            # If the unit contains a solved cell with the current value, continue to the next value.
            if unit.has_solved_cell_with_value(value):
                continue

            for n in range(0, 2):
                cn_pos = vertical_neighbours[n].get_distinct_column_containing_possible_val(value)
                if cn_pos is not None:
                    for i in [cn_pos, cn_pos + 3, cn_pos + 6]:
                        cell = unit.get_cells()[i]
                        if cell.has_possible_value(value):
                            cell.remove_possible_value(value)
                            updated = True

        return updated
