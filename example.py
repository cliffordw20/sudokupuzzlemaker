"""Example usage of SudokuPuzzleMaker.

This example uses the exactcover package at git+https://github.com/cliffordw20/exactcover.git.
Use the following command to install this package:

python -m pip install git+https://github.com/cliffordw20/exactcover.git
"""
from sudokupuzzlemaker import SudokuPuzzleMaker
from exactcover import solve as excsolve


if __name__ == "__main__":
    def solve_adapter(u, s):
        """Adapter for solve."""
        solution = excsolve(u, s, limit=1, randomize=True)
        return list(solution.pop())

    def count_adapter(u, s, preseed):
        """Adapter for count."""
        count = excsolve(u, s, limit=2, preseed=preseed, count=True)
        return count

    # Basic usage
    # Create a puzzle with 24 givens
    spm = SudokuPuzzleMaker(solve_adapter, count_adapter)
    result = spm.create_puzzle(24)
    print(result)
    print()
    # ('976.........4......5.6...3..6..5...15.2..8.9..3...25..8...157.4........8......1..', '976583412381429675254671839769354281542168397138792546823915764417236958695847123')

    # Create a puzzle with 24 givens and have black cells represented by '0'
    spm = SudokuPuzzleMaker(solve_adapter, count_adapter, blank='0')
    result = spm.create_puzzle(24)
    print(result)
    print()
    # ('004000700760020000030500900000950800005010000000600300807342009000080000001000040', '594831726768429135132567984273954861685213497419678352857342619946185273321796548')

    # It will take longer to create a puzzle with fewer givens. Run with more iterations for a
    # lower number of givens.
    spm = SudokuPuzzleMaker(solve_adapter, count_adapter)
    result = spm.create_puzzle(22, repeat=5, attempts=40, v=True)
    print(result)
    print()
    # sudokupuzzlemaker Solved Puzzle #1 of 5   (22 givens)
    # sudokupuzzlemaker #1 of 5: Attempt #0 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #1 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #2 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #3 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #4 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #5 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #6 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #7 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #8 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #9 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #10 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #11 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #12 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #13 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #14 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #15 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #16 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #17 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #18 of 40
    # sudokupuzzlemaker #1 of 5: Attempt #19 of 40
    # sudokupuzzlemaker Puzzle created.
    # ('4...72.....1....2...8...5..3.....6.8.9.4.........1.4...7.23.......5......36....84', '453172896961845723728369541314927658697458312285613479879234165142586937536791284')
