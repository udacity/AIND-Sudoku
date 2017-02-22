"""
Contains the functions and variables used in the solution.py file
"""
import logging
import sys

logging.basicConfig(filename='err_utils.log', level=logging.ERROR, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


# overriding the exception hook to log all errors in the log file
def excepthook(*args):
    logging.error('Uncaught exception:', exc_info=args)
    raise(args[0])

sys.excepthook = excepthook

digits = "123456789"
rows = "ABCDEFGHI"
cols = digits


# helper function to concatenate the rows and columns to create the three basic units
def cross(arr1, arr2):
    return [a+b for a in arr1 for b in arr2]


boxes = cross(rows, cols)
assert len(boxes) == 81, 'Number of boxes is not equal to 81'

row_units = [cross(row, cols) for row in rows]
assert len(row_units) == 9, 'Number of row units is not equal to 9'

column_units = [cross(rows, col) for col in cols]
assert len(column_units) == 9, 'Number of column units is not equal to 9'

square_units = [cross(row, col) for row in ['ABC', 'DEF', 'GHI'] for col in ['123', '456', '789']]
assert len(square_units) == 9, 'Number of square units is not equal to 9'

# isolating the diagonal elements A1,B2,C3....H8,I9 and A9,B8,C7....,H2,I1
diagonal_units = [list(map(lambda x: ''.join(x), zip(rows, cols))),
                  list(map(lambda x: ''.join(x), zip(rows, reversed(cols))))]
for diagonal_unit in diagonal_units:
    assert len(diagonal_unit) == 9, 'Number of boxes in the diagonal unit is not equal to 9'

# adding the diagonal elements to the unitlist and peers set so they are updated through constraint propagation
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

# storing the peers of each box in a dict
peers = dict((s, set(sum(units[s], []))-{s}) for s in boxes)
for box, box_peers in peers.items():
    if box == 'E5':
        assert len(box_peers) == 32, 'Number of peers for the central diagonal box {} is not 32'.format(box)
    elif box in [element for diagonal in diagonal_units for element in diagonal]:
        assert len(box_peers) == 26, 'Number of peers for the box {} lying on the diagonal is not 26'.format(box)
    else:
        assert len(box_peers) == 20, "Number of peers for the box {} is not 20".format(box)
