from copy import copy
import time
import os
import json
from validator import valid_board

def get_puzzle(level: str = 'easy') -> dict:
    result = os.popen(f"curl 'https://sudoku.com/api/level/{level}' \
        -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) \
        Gecko/20100101 Firefox/92.0' -H 'Accept: */*' -H \
        'Accept-Language: en-US,en;q=0.7,pl;q=0.3' --compressed -H \
        'X-Requested-With: XMLHttpRequest' -H 'DNT: 1' -H 'Alt-Used: sudoku.com' \
        -H 'Connection: keep-alive' -H 'Referer: https://sudoku.com/' -H \
        'Cookie: device_view=full; \
        mode=classic; checkMistakes=true; sdk_adw=1; sdk_analytics=1; sdk_confirm=1' -H \
        'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' \
        -H 'TE: trailers'")
    data = json.loads(result.read())
    return data

class Sudoku():
    # puzzle and solution are strings representing the sudoku board read from top-left to right
    def __init__(self, puzzle: str, solution: str) -> None:
        # on invalid input return an empty board
        if len(puzzle) != 81 or not puzzle.isnumeric():
            puzzle = '0' * 81
        if len(solution) != 81 or not solution.isnumeric():
            solution = '0' * 81

        self.puzzle = [int(i) for i in puzzle]
        self.solution = [int(i) for i in solution]
        
        self.__puzzle = puzzle
        self.__methods = {
            'backtracking' : self.__backtracking,
            'stochastic_search' : self.__stochastic_search,
            'constraint_programming' : self.__constraint_programming,
            'exact_cover' : self.__exact_conver,
            'relations_and_residuals' : self.__relations_and_residuals,
        }

        self.methods = self.__methods.keys()

    def validate_puzzle(self) -> bool:
        return valid_board(self.to_grid(self.puzzle))

    def check_with_solutions(self) -> bool:
        return self.puzzle == self.solution

    def to_grid(self, board = None):
        if board == None:
            board = self.puzzle

        return [([j for j in board[9 * i: (9 * (i + 1))]]) for i in range(9)]

    def pretty_print(self, board = None, print_zeros = False):
        grid = self.to_grid(board)

        for x, i in enumerate(grid):
            for y, j in enumerate(i):
                if j == 0 and not print_zeros:
                    j = '_'

                print(j, end = ' | ' if (y + 1) % 3 == 0 and y < len(i) - 1 else ' ')

            print()
            if (x + 1) % 3 == 0 and x < len(grid) - 1:
                print('-' * 21)
        
        print()

    def solve(self, option, stopwatch = False):
        if stopwatch:
            start = time.perf_counter_ns()

            if self.solve(option) == -1:
                return

            print(f'solving time: {time.perf_counter_ns() - start} ns')

        if not self.__methods.keys().__contains__(option):
            print('invalid option set')
            return -1

        self.__methods[option]()
    
    def reset_board(self):
        self.puzzle = [int(i) for i in self.__puzzle]

    def __backtracking(self):
        editable_positions = [x for x, i in enumerate(self.puzzle) if i == 0]
        ran = len(editable_positions)
        force_flag = False

        i = 0
        while (i < ran):
            #  valid && pos == 0
            # !valid && pos != 0
            while (self.validate_puzzle() == (self.puzzle[editable_positions[i]] == 0) or force_flag):
                if (self.puzzle[editable_positions[i]] >= 9):
                    self.puzzle[editable_positions[i]] = 0
                    i -= 2
                    force_flag = True
                    break
                
                self.puzzle[editable_positions[i]] += 1
                force_flag = False

            i += 1

    def __stochastic_search(self):
        print('stochastic')
    
    def __constraint_programming(self):
        print('contstraint programming')
    
    def __exact_conver(self):
        print('exact cover')
    
    def __relations_and_residuals(self):
        print('relations and residuals')

def main():
    difficulties = ['easy', 'medium', 'hard', 'expert', 'evil']

    puzzle = get_puzzle(difficulties[0])

    sudoku = Sudoku(puzzle['mission'], puzzle['solution'])
    sudoku.solve('backtracking', stopwatch = True)
    
    print('success' if sudoku.check_with_solutions() else 'failure')


if __name__ == '__main__':
    main()
