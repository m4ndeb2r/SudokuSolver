class HorizontalBlockSolver(object):

    @staticmethod
    def solve(unit):
        """Attempts to solve the specified unit by comparing it to its horizontal neighbour block units.
        Returns True if any cell was changed, or False otherwise."""
        updated = False
        if not unit.is_block_unit():
            return updated

        # TODO
        unit.get_horizontal_neighbours()

        return updated
