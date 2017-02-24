"""
Based from Udacity's solutions.
"""


rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [
    cross(rs, cs)
    for rs in ('ABC', 'DEF', 'GHI')
    for cs in ('123', '456', '789')]

diagonal_units = [
    [
        r + c
        for r_idx, r in enumerate(rows)
        for c_idx, c in enumerate(cols)
        if r_idx == c_idx],
    [
        r + c
        for r_idx, r in enumerate(rows)
        for c_idx, c in enumerate(reversed(list(cols)))
        if r_idx == c_idx]]

unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)

unitlist_with_diagonal = row_units + column_units + square_units + diagonal_units
units_with_diagonal = dict((s, [u for u in unitlist_with_diagonal if s in u]) for s in boxes)
peers_with_diagonal = dict((s, set(sum(units_with_diagonal[s],[])) - set([s])) for s in boxes)


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-'* (width * 3)] * 3)

    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print
