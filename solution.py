import utils
import copy


assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values, diagonal=False):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    twins = {}

    # Find all instances of naked twins
    for box, value in values.items():
        if len(value) == 2:
            for unit in (utils.units_with_diagonal if diagonal else utils.units)[box]:
                for test_box in unit:
                    if test_box != box and value == values[test_box]:
                        if not twins.get(test_box):
                            twins[box] = test_box

    def clean_naked_twin_val(values, box, naked_twin_value):
        value_to_clean = values[box]
        for char in naked_twin_value:
            value_to_clean = value_to_clean.replace(char, '')
        assign_value(
            values=values,
            box=box,
            value=value_to_clean)

    # Eliminate the naked twins as possibilities for their peers
    solution_values = values.copy()
    for box_1, box_2 in twins.items():
        for unit in (utils.units_with_diagonal if diagonal else utils.units)[box_1]:
            if box_2 in unit:
                for test_box in unit:
                    if test_box != box_1 and test_box != box_2:
                        clean_naked_twin_val(
                            values=solution_values,
                            box=test_box,
                            naked_twin_value=values[box_1])

    return solution_values


def grid_values(grid):
    """
    Based from Udacity's solutions.

    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
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
    return dict(zip(utils.boxes, chars))


def eliminate(values, diagonal=False):
    """
    Based from Udacity's solutions.

    Go through all the boxes, and whenever there is a box with a value,
    eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in (utils.peers_with_diagonal[box]
                     if diagonal else utils.peers[box]):
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values, diagonal=False):
    """
    Based from Udacity's solutions.

    Go through all the units, and whenever there is a unit with a value that
    only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in (utils.unitlist_with_diagonal if diagonal else utils.unitlist):
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values, diagonal=False):
    """
    Based from Udacity's solutions.

    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values, diagonal=diagonal)
        values = only_choice(values, diagonal=diagonal)
        values = naked_twins(values, diagonal=diagonal)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def is_puzzle_complete(values):
    for box, v in values.items():
        if len(v) > 1:
            return False
    return True


def search(values, diagonal=False):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    """
    values = reduce_puzzle(values, diagonal=diagonal)

    if not values:
        return False
    if is_puzzle_complete(values):
        return values

    base_box = min((box for box in values.keys() if len(values[box]) > 1), key=lambda box: len(values[box]))
    for option in values[base_box]:
        test_values = values.copy()
        test_values[base_box] = option
        test_values = reduce_puzzle(test_values)
        if test_values and is_puzzle_complete(test_values):
            return test_values

    for option in values[base_box]:
        test_values = values.copy()
        test_values[base_box] = option

        test_values = search(test_values)
        if test_values and is_puzzle_complete(test_values):
            return test_values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid.
        False if no solution exists.
    """
    values = grid_values(grid)
    return search(values, diagonal=True)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. ' +
              'Not a problem! It is not a requirement.')
