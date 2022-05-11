class SingleUnitSolver(object):

    @staticmethod
    def solve(unit):
        """Attempts to solve the specified unit internally.
        Returns True if any cell was changed, or False otherwise."""
        updated = False
        if not unit.is_solved():
            # Gather removable values
            removable_values = []
            for cell in unit.get_cells():
                if cell.is_solved():
                    removable_values.append(cell.get_solution())
            # Remove gathered values from other cells in unit
            for cell in unit.get_cells():
                if not cell.is_solved():
                    if cell.remove_possible_values(removable_values) > 0:
                        updated = True
        return updated
