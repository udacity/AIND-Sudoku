"""
Contains the functions and variables used in the solution.py file
"""

digits = "123456789"
rows = "ABCDEFGHI"
cols = digits

# helper function to concatenate the rows and columns to create the three basic units
def cross(A, B):
    return [a+b for a in A for b in B]


boxes = cross(rows, cols)
row_units = [cross(row, cols) for row in rows]
column_units = [cross(rows, col) for col in cols]
square_units = [cross(row, col) for row in ['ABC', 'DEF', 'GHI'] for col in ['123', '456', '789']]

# isolating the diagonal elements A1,B2,C3....H8,I9 and A9,B8,C7....,H2,I1
diagonal_units = [list(map(lambda x: ''.join(x), zip(rows, cols))),
                  list(map(lambda x: ''.join(x), zip(rows, reversed(cols))))]

# adding the diagonal elements to the unitlist and peers set so they are updated through constraint propagation
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

# storing the peers of each box in a dict
peers = dict((s, set(sum(units[s],[]))-{s}) for s in boxes)