# SudokuPuzzleMaker

The SudokuPuzzleMaker class creates sudoku puzzles.

## Basic Usage

A solver and a counting function needs to be supplied by the client. A puzzle is created by using `create_puzzle(num_givens)` which returns a tuple composed of a puzzle and its solution if a puzzle could be created, or `False` if one cannot be created. A valid puzzle is not guaranteed to be found, especially for a lower number of givens. The minumum number of givens for a valid puzzle is 17. However, it is unlikely a valid 17-given puzzle can be found for a particular completed grid.

```Python
# Create a puzzle with 24 givens
    spm = SudokuPuzzleMaker(solve_adapter, count_adapter)
    result = spm.create_puzzle(24)
    print(result)
    print()
    # ('976.........4......5.6...3..6..5...15.2..8.9..3...25..8...157.4........8......1..', '976583412381429675254671839769354281542168397138792546823915764417236958695847123')
```

---

## Reference

* __Cell Index__  
Cells are indexed from 0 to 80. The first row of the grid contains cell 0 to 8 with cell 0 in the top left corner and cell 8 in the top right corner of the grid. Cells 9 to 17 is the second row, and so on.

* __SudokuPuzzleMaker__(*solve, count, blank='.'*)  
Constructor

  * __Parameters__

    * __solve__(*u, s*) - A function that accepts two parameters and returns a solved sudoku puzzle.  
      * *u* - The first parameter is a set of 324 constraints to the sudoku exact cover problem.  
      Example: `{0, 1, ..., 80, ('r0', 0), ('r0', 1), ..., ('r8', 9), ('c0', 0), ('c0', 1), ..., ('c8', 9), ('b0', 0), ('b4', 1), ..., ('b8', 8), ('b8', 9)}`  
      * *s* - The second parameter is a dict of 729 candidates and their set of related constraints. A candidate's key is a tuple where the first item is the cell index and the second item is the number in that cell.  
      Example: `{(0, 1): {0, ('c0', 1), ('b0', 1), ('r0', 1)}, (0, 2): {0, ('b0', 2), ('c0', 2), ('r0', 2)}, ..., (80, 9): {80, ('c8', 9), ('b8', 9), ('r8', 9)}}`  
      * *Return* - The return is a list of 81 tuples. The first item of a tuple is the cell index and the second is the number in that cell. Example: `[(0, 1), (1, 8), (2, 2), ..., (80, 9)]`

    * __count__(*u, s, p*) - A function that returns the number of possible solutions of a given partial puzzle. If there is zero or more than one solution then the puzzle is not valid.  
      * *u* - The first parameter is a set of 324 constraints to the sudoku exact cover problem. See __solve__(*u, s*) for an example.  
      * *s* - The second parameter is a dict of 729 candidates and their set of related constraints. A candidate's key is a tuple where the first item is the cell index and the second item is the number in that cell. See __solve__(*u, s*) for an example.  
      * *p* - The third parameter is a set of tuples representing a partially solved puzzle. The first item of a tuple is the cell index and the second is the number in that cell.  
      Example: `{(0, 1), (33, 1), (23, 4), (31, 5), (45, 4), (56, 4), (20, 8), (14, 1), (59, 9), (41, 6), (18, 9), (54, 2), (75, 5), (10, 6), (70, 4), (48, 2), (15, 5), (64, 1), (72, 8), (1, 4), (12, 9), (43, 7), (26, 6), (37, 8), (61, 8)}`  
      * *Return* - An integer number of solutions to a partial puzzle. The return value is used to determine if there is more than one solution to a partial puzzle.

    * __blank__ - The character to denote a blank cell in a puzzle. *Default:* `'.'`

* SudokuPuzzleMaker.__create_puzzle__(*num_givens, repeat=1, attempts=20, v=False*)  
Create a valid 9x9 Sudoku puzzle.

  * __Return__ - A tuple that contains a sudoku puzzle and its solution, or `False` if a puzzle could not be created. The puzzle and solved puzzle are an 81-character string. Blank cells are represented by a `'.'` by default. The first 9 characters is the first row of the puzzle, the next 9 characters is the second row, and so on.
  Example:

    ```python
    ('.3..8...7.5.3...1.....26....65.....1.1.....8......4.3...4.1.89.3......26...9....3', '932581467756349218148726359465832971213697584897154632674213895389475126521968743')
    ```

  * __Parameters__
    * __num_givens__ - The desired number of givens in a puzzle.
    * __repeat__ - (Optional) The number of different solved puzzles to use to try to create a puzzle. *Default:* `1`
    * __attempts__ - (Optional) The number of attempts to make per each solved puzzle. *Default:* `20`
    * __v__ - (Optional) Boolean. When `True`, progress is printed to stderr. *Default:* `False`

* SudokuPuzzleMaker.__create_solved__()  
Creates a solved sudoku puzzle.

  * __Return__ - An 81-character string that represents a solved puzzle. The first 9 characters is the first row of the puzzle, the next 9 characters is the second row, and so on. Example:

    ```python
    '932581467756349218148726359465832971213697584897154632674213895389475126521968743'
    ```

---

## Example

See `example.py` for for an example of how to use SudokuPuzzleMaker.
