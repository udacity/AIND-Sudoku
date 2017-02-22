# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The `Naked Twins` strategy involves identifying all such boxes, within the same unit, that have the **exact same two 
digits** and eliminating those digits from the `peer set` that is **common to both those boxes**. 

This strategy follows the `Elimination` and `Only Choice` reduction techniques and can potentially solve more difficult
Sudoku problems without employing the `Search` technique.

When employed before the `Search` step, eliminating the naked twins can potentially reduce the number of recursions 
required to solve the Sudoku. This is of course a factor of the number of `Naked Twins` found in the problem. 

This function is thus implemented such that it plugs into the 'eliminate' and 'only_choice' function and returns the 
reduced Sudoku before every successive call to the `Search` function.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In a normal Sudoku, each box finds itself in three units namely `squares`, `rows` and `columns` and consequently has 
the **same number of peers**. However in the diagonal sudoku problem, all box elements forming the main diagonals i.e. 
`A1, B2, C3, D4, E5, F6, G7, H8, I9` and `I1, H2, G3, F4, D6, E5, C7, B8, A9` have an additional unit and a 
**greater peer count**. Box `E5`, which is common to both diagonals, has **32** peers while each of the other boxes 
forming the diagonals have **26** each.

The challenge in a diagonal Sudoku is to identify the peers for each of the diagonal boxes and apply the same `contraint
propogation` technique to eliminate digits from these peers in every successive step. The algorithm for all functions
thus remains unchanged and it is only the data structures `unitlist`, `units` and `peers` that have to be setup correctly.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.