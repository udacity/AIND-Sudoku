from visualize import visualize_assignments

assignments = []

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    pass

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '.' for empties."
    pass

def display(values):
    "Display these values as a 2-D grid."
    pass

def only_choice(values):
    pass

def single_possibility(values):
    pass

def reduce_puzzle(values):
    pass

def solve(grid):
    pass

def search(values):
    pass

diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
display(solve(grid_values(diag_sudoku_grid)))
visualize_assignments(assignments)
