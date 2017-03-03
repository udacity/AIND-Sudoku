from utils import *

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
    # Eliminate the naked twins as possibilities for their peers

    # filter the list of boxes that have exactly two digits
    possible_naked_twins = [box for box, val in values.items() if len(val) == 2]

    for box1, box2 in yieldtwins(possible_naked_twins, values):
        eliminate_twins(box1, box2, values)
    return values


def yieldtwins(possible_naked_twins, values):
    """

    :param possible_naked_twins: List containing all boxes with 2 digits
    :param values: Dict containing all sudoku values
    :return: tuple containing naked twins
    """
    # iterating through all boxes and finding the ones that are peers and whose digits match
    for i in range(len(possible_naked_twins)):
        # ensuring that the boxes aren't matched twice over
        for j in range(i+1, len(possible_naked_twins)):
            box1, box2 = (possible_naked_twins[i], possible_naked_twins[j])
            # condition: boxes need to be peers and contain the same two digits
            if box2 in peers[box1] and values[box1] == values[box2]:
                yield (box1, box2)


def eliminate_twins(box1, box2, values):
    """

    :param box1: string representation of the box containing first twin
    :param box2: string representation of the box containing second twin
    :param values: Dict containing all sudoku values
    :return: None
    """
    naked_digits = values[box1]
    # Set of all boxes that are common peers to the identified naked twins
    selected_peers = peers[box1].intersection(peers[box2])
    for peer in selected_peers:
        # replacing both the digits from the selected peers
        assign_value(values, peer, values[peer].replace(naked_digits[0], ''))
        assign_value(values, peer, values[peer].replace(naked_digits[1], ''))


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
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    """

    :param values:  The sudoku in dictionary form
    :return: Modified values (dict) after eliminating digits that are solved
    """

    # selecting only those boxes which have a single digit i.e. boxes that are solved
    selected_boxes = [box for box in boxes if len(values[box]) == 1]

    for box in selected_boxes:
        solved_digit = values[box]
        for peer in peers[box]:
            # eliminating the digit in the solved box from all its peers
            assign_value(values, peer, values[peer].replace(solved_digit, ''))
    return values


def only_choice(values):
    """

    :param values:  The sudoku in dictionary form
    :return: Modified values (dict)
    """
    for unit in unitlist:
        for box in unit:
            for char in values[box]:
                # for a given unit identify the box that has a unique digit and assign that digit to the box
                if not [s for s in unit if s != box and char in values[s]]:
                    assign_value(values, box, char)
                    break

    return values


def reduce_puzzle(values):
    """

    :param values:  The sudoku in dictionary form
    :return: Modified values (dict)
    """
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
    # "Using depth-first search combined with constraint propagation"
    # First, reduce the puzzle using the previous function
    new_values = reduce_puzzle(values)
    if new_values:
        val_array = [len(v) for v in new_values.values() if len(v) > 1]
        # Choosing the unfilled squares with the fewest possibilities but greater than 1
        if val_array:
            min_value = min(val_array)
            box = [square for square, value in new_values.items() if len(value) == min_value][0]
            # Using recursion to solve each one of the resulting sudokus
            # If a recursion path does not return False then these values are returned back to the calling function
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
