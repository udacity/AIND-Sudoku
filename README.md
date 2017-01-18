# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

### Install

This project requires **Python 2.7** and the following Python libraries installed:

- [NumPy](http://www.numpy.org/)
- [Pandas](http://pandas.pydata.org)
- [matplotlib](http://matplotlib.org/)
- [scikit-learn](http://scikit-learn.org/stable/)

You will also need to have software installed to run and execute an [iPython Notebook](http://ipython.org/notebook.html)

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 

##### Pygame

You also need to install pygame if you want to see your visualization. To do so simply run the following inside your conda env:

```conda install -c tlatorre pygame=1.9.2```

### Code

Template code is provided in the `sudoku_solver.ipynb` notebook file. You will also be required to use the included `sudoku.py` Python file and the `puzzles.txt` dataset file to complete your work. While some code has already been implemented to get you started, you will need to implement additional functionality when requested to successfully complete the project. If you are interested in how the visualizations are created in the notebook, please feel free to explore this Python file.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in function.py

### Run

In a terminal or command window, navigate to the top-level project directory `sudoku/` (that contains this README) and run one of the following commands:

```bash
ipython notebook sudoku_solver.ipynb
```  
or
```bash
jupyter notebook sudoku_solver.ipynb
```

This will open the iPython Notebook software and project file in your browser.

### Data

The data consists of a text file of diagonal sudokus for you to solve.