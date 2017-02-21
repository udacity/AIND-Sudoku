assignments = []
digits = "123456789"
rows = "ABCDEFGHI"
cols = digits


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
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
    possible_naked_twins = [box for box, val in values.items() if len(val) == 2]
    for i in range(len(possible_naked_twins)):
        for j in range(i+1, len(possible_naked_twins)):
            box1, box2 = (possible_naked_twins[i], possible_naked_twins[j])
            if box2 in peers[box1] and values[box1] == values[box2]:
                naked_digits = values[box1]
                selected_peers = peers[box1].intersection(peers[box2])
                for peer in selected_peers:
                    assign_value(values, peer, values[peer].replace(naked_digits[0], ''))
                    assign_value(values, peer, values[peer].replace(naked_digits[1], ''))
    return values


def cross(A, B):
    return [a+b for a in A for b in B]

boxes = cross(rows, cols)
row_units = [cross(row, cols) for row in rows]
column_units = [cross(rows, col) for col in cols]
square_units = [cross(row, col) for row in ['ABC', 'DEF', 'GHI'] for col in ['123', '456', '789']]
diagonal_units = [list(map(lambda x: ''.join(x), zip(rows, cols))),
                  list(map(lambda x: ''.join(x), zip(rows, reversed(cols))))]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-{s}) for s in boxes)


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

    values = dict(zip(boxes, grid))
    for key, value in values.items():
        if value is '.':
            values[key] = digits
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
    return

def eliminate(values):
    for box in boxes:
        digits = values[box]
        if len(digits) == 1:
            for peer in peers[box]:
                assign_value(values, peer, values[peer].replace(digits, ''))
    return values

def only_choice(values):
    for unit in unitlist:
        for box in unit:
            for char in values[box]:
                if not [s for s in unit if s!= box and char in values[s]]:
                    assign_value(values, box, char)
                    break

    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = naked_twins(only_choice(eliminate(values)))

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    new_values = reduce_puzzle(values)
    if new_values:
        val_array = [len(v) for v in new_values.values() if len(v) > 1]
        # Choose one of the unfilled squares with the fewest possibilities
        if val_array:
            min_value = min(val_array)
            box = [square for square, value in new_values.items() if len(value) == min_value][0]
            # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
            for digit in values[box]:
                temp = new_values.copy()
                temp[box] = digit
                temp = search(temp)
                if temp:
                    new_values = temp
                    return search(new_values)

        else:
            return new_values

def solve(grid):

    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))



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
