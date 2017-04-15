from collections import Counter
assignments = []
cols = "123456789"
rows = "ABCDEFGHI"
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
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        two_value_values = [ values[box] for box in unit if len(values[box]) == 2 ]
        c = Counter(two_value_values)
        for value, count in c.items():
            if count == 2: # find twin values
                for box in unit :
                    if values[box] != value:
                        assign_value(values, box, values[box].replace(value[0], '').replace(value[1],""))
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [ a+b for a in A for b in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows,c ) for c in cols]
square_units = [ cross(rs , cs) for rs in ("ABC", "DEF", "GHI") for cs in ('123', '456','789')]
diag_units =[[ rows[i]+cols[i] for i in range(0,9)],[ rows[i] + cols[8-i] for i in range(0,9)]]
unitlist = row_units + col_units + square_units + diag_units
units = dict((s,[ u for u in unitlist if s in u ]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

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
    if len(grid) != 81 or len(boxes) != 81:
        exit(1)

    values = {}
    for index, box in enumerate(boxes):
        #values[value] = grid[index]
        value = grid[index] if grid[index] != "." else "123456789"
        assign_value(values, box, value)

    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    for box, value in values.items():
        if len(value) == 1:
            for peer in peers[box]:
                #values[peer] = values[peer].replace(value, '')
                assign_value(values,peer, values[peer].replace(value, ''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [ box for box in unit if digit in values[box]]
            if len(dplaces)==1:
                #values[dplaces[0]] = digit
                assign_value(values,dplaces[0],digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # use twins strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        #new_sudoku[s] = value
        assign_value(new_sudoku, s, value)
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
    ret = search(grid_values(grid))
    if ret:
        return ret

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
