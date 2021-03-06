from board.board_exception import BoardException


class Cell(object):

    def __init__(self):
        self.__possible_values = []
        for i in range(1, 10):
            self.__possible_values.append(i)

    # Validates the cell, e.g. checks the (number of) possible values.
    def validate(self):
        length = len(self.__possible_values)
        if length < 1 or length > 9:
            raise BoardException(f"Number of possible values for this cell is incorrect ({length}).")
        for possible_value in self.__possible_values:
            if possible_value not in range(1, 10):
                raise BoardException(f"Value {possible_value} is not a valid value for this cell.")

    # Returns if the specified value is a possible solution for the cell.
    def has_possible_value(self, value):
        return value in self.__possible_values

    # Returns if the possible values for the cell.
    def get_possible_values(self):
        return self.__possible_values

    # Removes the specified value from the list of possible values (if it exists).
    # Returns True on success, or False otherwise.
    def remove_possible_value(self, value):
        if value in self.__possible_values:
            if len(self.__possible_values) == 1:
                raise BoardException("Unexpected program error: attempting to remove a value from a solved cell.")
            self.__possible_values.remove(value)
            return True
        return False

    # Removes the specified values from the list of possible values (if present).
    # Returns the number of removed values."""
    def remove_possible_values(self, values):
        removed = 0
        for value in values:
            if self.remove_possible_value(value):
                removed += 1
        return removed

    # Sets a definitive value for the cell.
    def set_value(self, value):
        int_value = int(value)
        if int_value < 1 or int_value > 9:
            raise BoardException("Cell can only contain values in range 1 to 9.")
        self.__possible_values = [int(value)]

    # Determines if the cell is solved, e.g. has a single definitive value.
    def is_solved(self):
        return len(self.__possible_values) == 1

    # Returns the solution for this cell, or None if the cell is not (yet) solved.
    def get_solution(self):
        if self.is_solved():
            return self.__possible_values[0]
        return None

    # Returns a string representation of the cell.
    def to_string(self):
        if self.is_solved():
            return f" {self.__possible_values[0]} "
        else:
            return " . "
