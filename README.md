# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The Naked Twins problem states that when any two peers have the same possible values (of length 2), all other boxes in the same unit can have those possible values removed (if the box has not yet been solved). Using Contstraint Propagation, the boxes to change and both equal peers must be in the same unit. Thus, logic states each unit containing the pair of equal valued peers must be found. Each box within that unit can have it's possible values reduced by removing the values in the identical pair, if the box has not yet already been solved (value of length 1). Using the units where the naked twins exist shows how Constraint Propogation is narrowing the search space, allowing for quicker computation and less possibilities to consider.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The Diagonal Sudoku problem states that the diagonal units (i.e. A1, B2, C3….I9 and A9, B8, C7…I1) must also consist of distinct values of 1 to 9. This is in fact adding another constraint to the Sudoku board, which limits the search space and reduces the number of possibilties. To add this constraint to the list of constraints, each diagonal is listed and added to the units list. The elimination, only choice, search and naked twins problems will then all adhere to the new constraint. This shows that introducing new constraints limits the search space and reduces the number of possible solutions on the Sudoku board.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.