import random

from board.board import Board
from sudoku_exception import SudokuException

board = None

choice = '0'
while choice not in ['1', '2', '3']:
    print("\n\n*** SUDOKU ***\n")
    print("You can either choose to have the program solve a predefined board")
    print("or you can enter a board manually.\n")
    print("Pick a number from the menu:\n")
    print("\t[1] Solve a predefined board")
    print("\t[2] Let me enter a board manually")
    print("\t[3] Get me out of here!\n")
    choice = input("Enter your choice: ")
    if choice == '3':
        print("\nBye! See you soon!")
        quit()

if choice == '1':
    # Only one preset for now ...
    presets = [
        [
            '....1....',
            '...257...',
            '.........',
            '2.4...7.5',
            '...5.9...',
            '3.8...2.1',
            '.........',
            '...762...',
            '....8....'
#        ], [
#            '.7.1.....',
#            '.......5.',
#            '..6...4.3',
#            '.........',
#            '5...4.82.',
#            '..963...4',
#            '...32....',
#            '28.7.....',
#            '65......9'
#            #        ], [
##            '.57....68',
#            '683......',
#            '1..896...',
#            '..846..9.',
#            '74.9..35.',
#            '3...17.46',
#            '4...5..8.',
#            '2.918.573',
#            '.35.72...'
#        ], [
#            '....9..16',
#            '..7..6.42',
#            '..8..7...',
#            '135...9..',
#            '...18.5..',
#            '........7',
#            '3567....1',
#            '..9....3.',
#            '8...3....'
#        ], [
#            '......234',
#            '........5',
#            '.....1789',
#            '1........',
#            '.........',
#            '.........',
#            '257......',
#            '3.9......',
#            '4.6......'
#        ], [
#            '......234',
#            '........5',
#            '..5...789',
#            '1........',
#            '.........',
#            '.........',
#            '257......',
#            '3.9......',
#            '4.6......'
#        ], [
#            '......1..',
#            '.........',
#            '.........',
#            '.........',
#            '.........',
#            '........3',
#            '1........',
#            '.........',
#            '......234'
#        ], [
#            '...567234',
#            '...349...',
#            '...2..567',
#            '632......',
#            '.58......',
#            '.94......',
#            '2.5......',
#            '3.6......',
#            '4.7......'
#        ], [
#            '3........',
#            '4........',
#            '5........',
#            '6........',
#            '7........',
#            '8.9......',
#            '...9.....',
#            '.........',
#            '...345678'
        ]
    ]

    # Pick a random preset ...
    rows = presets[random.randint(0, len(presets) - 1)]
    # Create a new Sudoku board
    board = Board(rows)

if choice == '2':
    print("Enter initial board settings, row by row.")
    print("Enter the digit of a cell, or a '.' for an empty cell.")
    print("Every row contains 9 cells, and the board contains 9 rows.")
    print("For example, a row might be entered as: ..5..6.8.")
    print("Or an initial board as: ")
    print("\t.7.1.....")
    print("\t.......5.")
    print("\t..6...4.3")
    print("\t.........")
    print("\t5...4.82.")
    print("\t..963...4")
    print("\t...32....")
    print("\t28.7.....")
    print("\t65......9\n")

    # Let user enter the initial settings of the board, and update the board
    # An exception is raised when illegal input is detected.
    rows = []
    for row_index in range(0, 9):
        row = input(f"Enter row {row_index + 1}: ")
        rows.append(row)
    # Create a new Sudoku board
    board = Board(rows)

# Print the initial board.
print('-' * 27)
board.print()

# Try to solve the sudoku and print the result
try:
    board = board.solve()
    if board.is_solved():
        print("\nYay!! Solved it!!")
    else:
        print("\nSorry, too hard to solve ... :(")
except SudokuException as se:
    print("\nOops! The board became invalid. (Was the initial setting okay?)")
    choice = input("Show error details? [y/n]: ")
    if choice in ['y', 'Y']:
        print(se)
print('-' * 27)
board.print()
print('-' * 27)

