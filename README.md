# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The `Naked Twins` strategy involves identifying all such boxes, within the same unit, that have the **exact same two 
digits** and eliminating those digits from the `peer set` that is **common to both those boxes**. 
This strategy follows the `Elimination` and `Only Choice` reduction techniques and can potentially solve more difficult
Sudoku problems without employing the `Search` technique.
When employed before the `Search` step, eliminating naked twins reduces the number of recursions required to solve the 
Sudoku.
This function is thus implemented such that it plugs into the 'eliminate' and 'only_choice' function and returns the 
reduced Sudoku before every successive call to the `Search` function. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In addition to the rows, columns and square units, we need to isolate the `diagonal` elements and add them to the 
   `peers` set. Once we have these set up, their values are modified in much the same way as the other elements in
   the `peers` set, through successive stages of `constraint propagation` and `search`.

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