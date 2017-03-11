from board import Board

sample_start = [[None, None, [], [], [], [], None, None],
                [None, ['R'],   ['R'], ['G'], ['G'], ['R'], ['R'],   None],
                [[],   ['G'],   ['G'], ['R'], ['R'], ['G'], ['G'],   []],
                [[],   ['R'],   ['R'], ['G'], ['G'], ['R'], ['R'],   []],
                [[],   ['G'],   ['G'], ['R'], ['R'], ['G'], ['G'],   []],
                [[],   ['R'],   ['R'], ['G'], ['G'], ['R'], ['R'],   []],
                [None, ['G'],   ['G'], ['R'], ['R'], ['G'], ['G'],   None],
                [None, None, [], [], [], [], None, None]]

board = Board(sample_start)
print board
board = board.make_move('R', (1, 1, 1), (2, 1))
board = board.make_move('R', (2, 1, 2), (3, 1))
board = board.make_move('R', (3, 1, 3), (4, 1))
board = board.make_move('R', (4, 1, 4), (5, 1))
board = board.make_move('R', (5, 1, 5), (6, 1))
print board
