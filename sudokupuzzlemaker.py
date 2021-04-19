"""Sudoku Puzzle Maker."""
from random import shuffle
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)


class SudokuPuzzleMaker:
    """The SudokuPuzzleMaker class creates sudoku puzzles."""

    def __init__(self, solve, count, blank='.'):
        """Set up constraints, candidates, and logger.

        Args:
            solve:
                A function, solve(u, s), that accepts two parameters and returns a solved sudoku
                puzzle.

                The first parameter is a set of 324 constraints to the sudoku exact cover problem.
                Example: '{0, 1, ..., 80, ('r0', 0), ('r0', 1), ..., ('r8', 9), ('c0', 0),
                ('c0', 1), ..., ('c8', 9), ('b0', 0), ('b4', 1), ..., ('b8', 8), ('b8', 9)}'.

                The second parameter is a dict of 729 candidates and their set of related
                constraints. A candidate's key is a tuple where the first item is the cell index
                and the second item is the number in that cell.
                Example: '{(0, 1): {0, ('c0', 1), ('b0', 1), ('r0', 1)}, (0, 2): {0, ('b0', 2),
                ('c0', 2), ('r0', 2)}, ..., (80, 9): {80, ('c8', 9), ('b8', 9), ('r8', 9)}}'

                The return is a list of 81 tuples. The first item of a tuple is the cell index and
                the second is the number in that cell.
                Example: '[(0, 1), (1, 8), (2, 2), ..., (80, 9)]'

            count:
                A function, count(u, s, p), that counts the number of possible solutions of a given
                partial puzzle. If there is zero or more than one solution then the puzzle is not
                valid. The first parameter is a set of 324 constraints to the sudoku exact cover
                problem. See 'solve' for an example.

                The second parameter is a dict of 729 candidates and their set of related
                constraints. A candidate's key is a tuple where the first item is the cell index
                and the second item is the number in that cell. See 'solve' for an
                example.

                The third parameter is a set of tuples representing a partially solved puzzle. The
                first item of a tuple is the cell index and the second is the number in that cell.
                Example: '{(0, 1), (33, 1), (23, 4), (31, 5), (45, 4), (56, 4), (20, 8), (14, 1),
                (59, 9), (41, 6), (18, 9), (54, 2), (75, 5), (10, 6), (70, 4), (48, 2), (15, 5),
                (64, 1), (72, 8), (1, 4), (12, 9), (43, 7), (26, 6), (37, 8), (61, 8)}'

            blank:
                The character to denote a blank cell in a puzzle.
        """
        self.solve = solve
        self.count = count
        self.blank = blank
        self._map_cell_to_box()
        self._init_constraints()
        self._init_candidates()
        self.logger = logging.getLogger(__name__)

    def _init_constraints(self):
        """Constraints.

        There are 324 constraints to the sudoku exact cover problem. Each cell must contain one
        number between 1 through 9. Each group (i.e. a row, column, or box) must contain each
        number between 1 through 9 exactly once. Cell constraints are represented as the cell
        number. Group constraints are a tuple containing the row, column, or box number and number.

        Cell: {0, 1, ... 80}
        Row: {('c0', 1), ... ('c0', 9)}
        Column: {('r0', 1), ... ('r8', 9)}
        Box: {('b0', 1), ... ('b8', 9)}
        """
        self.constraints = set()
        self.constraints |= {i for i in range(81)}
        self.constraints |= {(f'{a}{i}', n) for a in 'rc' for i in range(9)
                             for n in range(1, 10)}
        self.constraints |= {(f'b{i}', n) for i in range(9)
                             for n in range(1, 10)}

    def _init_candidates(self):
        """Candidates.

        There are 729 candidates to the problem. The candidates are represented as a dict where a
        candidate's key is a tuple of the cell index and the number in that cell. A candidate's
        value is a set of the key's related constraints.

        {(0, 1): {0, ('b0', 1), ('r0', 1), ('c0', 1)},
         (0, 2): {0, ('r0', 2), ('b0', 2), ('c0', 2)}, ...
         (80, 9): {80, ('b8', 9), ('r8', 9), ('c8', 9)}}
        """
        self.candidates = {(i, n): {(i),
                           (f'r{i // 9}', n), (f'c{i % 9}', n),
                           (f'b{self.boxn[i]}', n)}
                           for i in range(81) for n in range(1, 10)}

    def _map_cell_to_box(self):
        self.boxn = {i: (3 * (i // 27)) + ((i % 9) // 3) for i in range(81)}

    def _remove_nums(self):
        """Remove numbers from a solved puzzle until a vaild puzzle or no valid puzzle is found."""
        if len(self.removed) >= 81 - self.num_givens:
            # Found a good puzzle
            self.puzzle.extend(self.forbid)
            return True
        if len(self.puzzle) == 0:
            return False
        forbid_count = 0
        while (len(self.removed) < 81 - self.num_givens and
               len(self.forbid) < self.num_givens):
            self.removed.append(self.puzzle.pop())
            count = self.count(self.constraints, self.candidates,
                               preseed=set(self.puzzle) | set(self.forbid))
            if count > 1:
                # Puzzle should not have more than one solution
                self.forbid.append(self.removed.pop())
                forbid_count += 1
                continue
            if self._remove_nums() is False:
                # Children have no solution. Try another number.
                self.forbid.append(self.removed.pop())
                continue
            # child found a good puzzle
            return True

        # This level has no solution
        for i in range(forbid_count):
            self.puzzle.append(self.forbid.pop())
        return False

    def _to_string(self, puzzle):
        a = [self.blank] * 81
        for n in puzzle:
            a[n[0]] = n[1]
        return ''.join(map(str, a))

    def create_solved(self):
        """Create a valid solved 9x9 Sudoku puzzle.

        Returns:
            str: The solved puzzle is an 81-character string. Blank cells are represented by a '.'
            by default. The first 9 characters is the first row of the puzzle, the next
            9 characters is the second row, and so on.
        """
        self.solved_puzzle = self.solve(self.constraints, self.candidates)
        self.solved_puzzle.sort()
        return self._to_string(self.solved_puzzle)

    def _create_puzzle_from_solved(self, num_givens):
        self.num_givens = num_givens
        self.removed = []
        self.forbid = []
        self.puzzle = self.solved_puzzle.copy()
        shuffle(self.puzzle)
        result = self._remove_nums()
        if result:
            return self.puzzle
        self.puzzle = []
        return False

    def create_puzzle(self, num_givens, repeat=1, attempts=20, v=False):
        """Create a valid 9x9 Sudoku puzzle.

        Args:
            num_givens:
                The desired number of givens in a puzzle.
            repeat:
                (Optional) The number of different solved puzzles to use to try to create a puzzle.
            attempts:
                (Optional) The number of attempts to make per each solved puzzle.
            v:
                (Optional) Boolean. When 'True', progress is logged to stderr.

        Returns:
            Tuple[str, str] | False: A tuple that contains a sudoku puzzle and its solution, or
            'False' if a puzzle could not be created. The puzzle and solved puzzle are
            81-character strings. Blank cells are represented by a '.' by default. The first
            9 characters is the first row of the puzzle, the next 9 characters is the second row,
            and so on.
        """
        if v is True:
            log_level = logging.INFO
        else:
            log_level = logging.DEBUG
        for repitition in range(repeat):
            fail_count = 0
            num_attempts = attempts
            self.create_solved()
            self.logger.log(log_level, f'Solved Puzzle #{repitition + 1} of {repeat}   '
                                       f'({num_givens} givens)')
            for attempt in range(num_attempts):
                self.logger.log(log_level, f'#{repitition + 1} of {repeat}: Attempt #{attempt} of '
                                           f'{num_attempts}')
                result = self._create_puzzle_from_solved(num_givens)
                if result:
                    self.logger.log(log_level, 'Puzzle created.')
                    return (self._to_string(self.puzzle),
                            self._to_string(self.solved_puzzle))
                fail_count += 1
        return False


if __name__ == '__main__':
    pass
