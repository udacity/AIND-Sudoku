from collections import defaultdict

assignments = []

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
    nt = []
    # For each unit
    for unit in unitlist:
        # Fill the cells with some set of values
        values2cell = defaultdict(set)
        for cell in unit:
            values2cell[values[cell]].add(cell)
        # If there is a set of cells having the same possibble values 
        # and the number of possible values is the same as the power of the set
        for (vals, cells) in iter(values2cell.items()):
            # Limitation of size == 2 for naked twins set is required for passing the unit tests
            # Actually without the len(vals) == 2 condition solution will be more general and constraint more restrictive 
            if len(vals) == len(cells) and len(vals) == 2:
               # It is a naked twins for the unit - these values should be distributed amongst the cells
               nt.append((unit, vals, cells)) 
    
    # Eliminate the naked twins as possibilities for their peers
    for (unit, vals, cells) in iter(nt):
        for cell in unit:
            # Check it is not a cell of current naked twins
            if cell not in cells:
                 # Remove naked twins values from its unit
                 for v in vals:
                     assign_value(values, cell, values[cell].replace(v, ''))
    return values     

def cross(A, B):
    """Cross product of elements in A and elements in B.
    Args:
        A, B - arrays of values
    Returns:
        cross product of values in A and B
    """
    res = []
    for a in A:
        for b in B:
          res.append(a + b)
    return res

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[rows[i]+cols[i] for i in range(len(rows))], [rows[len(rows) - i - 1]+cols[i] for i in range(len(rows))]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
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
    res = dict()
    for i in range(len(grid)):
        if grid[i] == '.':
            assign_value(res, boxes[i], '123456789')
        else:
            assign_value(res, boxes[i], grid[i])
    return res

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    It is not a part of the project, so I just copied it from utils
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return              

def eliminate(values):
    """Use eliminate strategy to reduce the possibilities of cell values:
       find a cell with known value and remove this value from its peers
    Args:
        values(dict): The sudoku in dictionary form
    """
    res = values
    for (k, v) in iter(values.items()):
        if len(v) == 1:
            for p in peers[k]:
                assign_value(res, p, res[p].replace(v, ''))
    return res

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    new_values = values.copy()  # note: do not modify original values
    for unit in unitlist:
        choices = defaultdict(set)
        for cell in unit:
            for v in values[cell]:
                choices[v].add(cell)
        for (k, v) in iter(choices.items()):
            if len(v) == 1:
                for cell in v:
                    if len(new_values[cell]) > 1:
                        assign_value(new_values, cell, k)
    return new_values    

def reduce_puzzle(values):
    """Apply all the constraints propagation techniques iteratively until we've solved the puzzle 
    or we've stalled - i.e. new iteration doesn't change our values

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after reducing the puzzle.        
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Use the Only Choice Strategy
        values = only_choice(values)

	# Use the Naked Twins Strategy
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
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    
    values = reduce_puzzle(values)
    if values == False:
        return False
    
    # Choose one of the unfilled squares with the fewest possibilities
    min_choice = ''
    min_cell = ''
    for (cell, val) in iter(values.items()):
        if len(val) > 1:
            if min_choice == '' or len(min_choice) > len(val):
                min_choice = val
                min_cell = cell
    
    if min_choice == '':
        return values
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    
    for v in min_choice:
        tmp_values = values.copy()        
        assign_value(tmp_values, min_cell, v)
        new_values = search(tmp_values)
        if new_values != False:
            return new_values
    return False

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
