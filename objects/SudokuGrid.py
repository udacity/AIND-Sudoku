import random

class SudokuGrid:
    """A class to generate and check Sudoku data."""
    def __init__(self):
        """Builds a default, totally empty grid."""
        self.grid = []
        temp = []
        for x in range(9):
            temp.append(None)
        for y in range(9):
            self.grid.append(temp[:])
    
    def getNum(self, row, column):
        """Get a number at a specific position.
        Takes a row and a column."""
        return self.grid[row][column]
        
    def setNum(self, row, column, number):
        """Set a number at a specific position.
        Takes a row and a column."""
        self.grid[row][column] = number

    def checkRow(self, row, number):
        """Check for a number within a row.
        Takes a row to look in and a number to check for."""
        for x in range(9):
            if self.getNum(row, x) == number:
                return True
        return False
    
    def checkColumn(self, column, number):
        """Check for a number within a column.
        Takes a column to look in and a number to check for."""
        for y in range(9):
            if self.getNum(y, column) == number:
                return True
        return False
        
    def checkSquare(self, row, column, number):
        """Check for a number within a square.
        Takes a row and column to look in and a number to check for."""
        if row in (0, 1, 2): rowrange = (0, 1, 2)
        if row in (3, 4, 5): rowrange = (3, 4, 5)
        if row in (6, 7, 8): rowrange = (6, 7, 8)
        if column in (0, 1, 2): colrange = (0, 1, 2)
        if column in (3, 4, 5): colrange = (3, 4, 5)
        if column in (6, 7, 8): colrange = (6, 7, 8)
        
        for y in rowrange:
            for x in colrange:
                if self.getNum(y, x) == number:
                    return True
        return False
    
    def checkAll(self, row, column, number):
        """Performs all three (row, column and square) checks.
        Takes a row and column to look in and a number to check for."""
        if self.checkRow(row, number):
            return True
        elif self.checkColumn(column, number):
            return True
        elif self.checkSquare(row, column, number):
            return True
        else:
            return False
        
    def printGrid(self):
        """Provides a decent print for debugging at the console."""
        print
        for y in range(9):
            for x in range(9):
                if x in (3, 6):
                    print "|",
                temp = self.getNum(y, x)
                if temp == None:
                    print " ",
                else:
                    print temp,
            if y in (2, 5):
                print
                print "-" * 22
            else:
                print
        print

    def createGrid(self, genAmount=81, theSeed=None):
        """Use a simple method to generate a puzzle.
        Takes numToGen to place that number of elements 
        on the grid."""
        random.seed(theSeed)
        
        avail = []
        for num in range(0, 81):
            avail.append((num % 9) + 1)

        while len(avail) > 40:
            location = int(random.random() * len(avail))
            numToPlace = avail[location]
            row = int(random.random() * 9)
            col = int(random.random() * 9)
            
            # print "Trying to place %s at [ %s, %s ]" % (numToPlace, row, col)
            
            if self.getNum(row, col) == None:
                if not self.checkAll(row, col, numToPlace):
                    self.setNum(row, col, numToPlace)
                    # print "Success!"
                    del avail[location]
                # else:
                    # self.printGrid()
            # else:
                # self.printGrid()
    
    def checkSolution(self, solution):
        for row in range(9):
            for col in range(9):
                if not solution.getNum(row, col) == self.getNum(row, col):
                    return False
        return True
        

if __name__ == "__main__":
    print "Testing SudokuGrid functionality."
    print "Create an empty grid..."
    sampleGrid = SudokuGrid()
    sampleGrid.printGrid()
    
    # print
    # print "Compare an empty grid to another empty grid..."
    # emptyGrid = SudokuGrid()
    # print sampleGrid.checkSolution(emptyGrid)

    # print
    # print "Set three numbers in an empty grid..."
    # sampleGrid.setNum(0, 0, 1)
    # sampleGrid.setNum(0, 1, 2)
    # sampleGrid.setNum(0, 2, 3)
    # sampleGrid.setNum(0, 3, 1)
    # sampleGrid.printGrid()
    # print "Check row for ones...",
    # print sampleGrid.checkRow(0, 1)
    # print "Check row for nines...",
    # print sampleGrid.checkRow(0, 4)
    # sampleGrid.setNum(1, 0, 4)
    # sampleGrid.setNum(2, 0, 5)
    # sampleGrid.setNum(3, 0, 6)
    # sampleGrid.printGrid()
    # print "Check column for ones...",
    # print sampleGrid.checkColumn(0, 1)
    # print "Check column for nines...",
    # print sampleGrid.checkColumn(0, 9)
    # sampleGrid.setNum(2, 2, 1)
    # sampleGrid.printGrid()
    # print "Check square for ones...",
    # print sampleGrid.checkSquare(0, 0, 1)
    # print "Check square for nines...",
    # print sampleGrid.checkSquare(0, 0, 9)
    
    print
    print "Attempting to create a full solution..."
    sampleGrid.createGrid(81)
    print
    print
    print "DONE!"
    sampleGrid.printGrid()
    
    # print
    # sampleGrid2 = SudokuGrid()
    # sampleGrid2.createGrid(81, 10)
    # sampleGrid2.printGrid()
