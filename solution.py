'''
** Naked twins implementation understanding. **
In the README.md file, the student has shown an understanding of how constraint propagation
has been used to implement the naked twins function, by enforcing the constraint
that no squares outside the two naked twins squares can contain the twin values

** Diagonal Sudoku implementation understanding. **
In the README.md file, the student has shown an understanding of how constraint propagation
has been used to solve the diagonal sudoku, by adding the diagonals to the set of constraints.
'''

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

# Create new peers values to include diagonal
diag_units_down = []
diag_units_up = []
row_ind = 1
for row in row_units:
    diag_units_down.append(row[row_ind-1])
    diag_units_up.append(row[len(row)-row_ind])
    row_ind = row_ind+1

for box in diag_units_down:
    peers[box] = list(peers[box])
    peers[box].extend(diag_units_down)
    peers[box].remove(box)
    peers[box] = sorted(set(peers[box]))  # this is to remove duplicate items in list

for box in diag_units_up:
    peers[box] = list(peers[box])
    peers[box].extend(diag_units_up)
    peers[box].remove(box)
    peers[box] = sorted(set(peers[box]))  # this is to remove duplicate items in list

# TODO please make use of this function
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    '''
    In the README.md file, the student has shown an understanding of how constraint propagation
    has been used to implement the naked twins function, by enforcing the constraint
     that no squares outside the two naked twins squares can contain the twin values
    '''

    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    boxes_morethan_1d = [s for s in boxes if len(values[s]) > 1]
    for box in boxes_morethan_1d:
        # check column
        for column_unit in column_units[int(box[1])-1]:
            if (box != column_unit):
                if (values[box] == values[column_unit] and len(values[box]) == 2):
                    to_be_elim_boxes = [s for s in column_units[int(box[1]) - 1] if len(values[s]) > len(values[box])]
                    for char in values[box]:
                        for elim_box in to_be_elim_boxes:
                            assign_value(values, elim_box, values[elim_box].replace(char, ''))
            else:
                pass

        # check row
        if(box[0] == 'A'):
            row = 0
        elif(box[0] == 'B'):
            row = 1
        elif (box[0] == 'C'):
            row = 2
        elif (box[0] == 'D'):
            row = 3
        elif (box[0] == 'E'):
            row = 4
        elif (box[0] == 'F'):
            row = 5
        elif (box[0] == 'G'):
            row = 6
        elif (box[0] == 'H'):
            row = 7
        elif (box[0] == 'I'):
            row = 8

        for row_unit in row_units[row]:
            if (box != row_unit):
                 if (values[box] == values[row_unit] and len(values[box]) == 2):
                    to_be_elim_boxes = [s for s in row_units[row] if len(values[s]) > len(values[box])]
                    for char in values[box]:
                        for elim_box in to_be_elim_boxes:
                            assign_value(values, elim_box, values[elim_box].replace(char, ''))
            else:
                pass

    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    # solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # print("solved_values_before: {}".format(solved_values_before))
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # print("solved_values_after: {}".format(solved_values_after))
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False  ## Failed earlier

    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = search(grid_values(grid))
    return values

if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
