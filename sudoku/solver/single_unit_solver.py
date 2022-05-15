from collections import defaultdict


class SingleUnitSolver(object):

    # Attempts to solve the specified unit internally.
    # Returns True if any cell was changed, or False otherwise.
    @staticmethod
    def solve(unit):
        updated = False
        for n in range(1, 9):
            # Gather cells with n possible values, and store them in a
            # 2D-dictionary. The outer key of the dictionary is based
            # on the combination of the (n) possible values, and the
            # inner key is the cell key on the board.
            outer_dict = defaultdict(dict)
            for key in unit.get_cell_keys():
                cell = unit.get_cell(key)
                values = cell.get_possible_values()
                if len(values) == n:
                    outer_key = ''.join([str(v) for v in values])
                    outer_dict[outer_key][key] = cell

            # Now, we have the cells with n possible values grouped
            # together. If there are exactly n cells with the exact
            # same combination of possible values, we can be sure that
            # no other cell in the unit will have either of these values
            # as a solution. We can therefore remove them from those
            # other cells' possible values.
            for inner_dict in outer_dict.values():
                if len(inner_dict.values()) == n:
                    for cell_key in unit.get_cell_keys():
                        if cell_key not in inner_dict.keys():
                            for cell_with_removable_values in inner_dict.values():
                                size_before = len(unit.get_cell(cell_key).get_possible_values())
                                unit.get_cell(cell_key).remove_possible_values(cell_with_removable_values.get_possible_values())
                                size_after = len(unit.get_cell(cell_key).get_possible_values())
                                updated = updated or (size_before > size_after)
        return updated

#   # Attempts to solve the specified unit internally.
#   # Returns True if any cell was changed, or False otherwise.
#   @staticmethod
#   def solve_old(unit):
#       updated = False
#       if unit.is_solved():
#           return updated

#       # Gather removable values
#       removable_values = []
#       for cell in unit.get_cells():
#           if cell.is_solved():
#               removable_values.append(cell.get_solution())
#       # Remove gathered values from other cells in unit
#       for cell in unit.get_cells():
#           if not cell.is_solved():
#               if cell.remove_possible_values(removable_values) > 0:
#                   updated = True

#       return updated

