class VerticalBlockSolver(object):

    @staticmethod
    def solve(unit):
        """Attempts to solve the specified unit by comparing it to its vertical neighbour block units.
        Returns True if any cell was changed, or False otherwise."""
        updated = False
        if not unit.is_block_unit():
            return updated

        # TODO
        unit.get_vertical_neighbours()

        return updated
