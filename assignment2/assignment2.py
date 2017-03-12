from board import Board
from player import Player

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

print "Starting Computer vs Computer Game"


def heuristic1(player):
    return 0


def heuristic2(player):
    return 0


print "Player 1 is R and will play first"
print "Would you like to use heuristic 1 or 2 for Player 1?"
option = int(raw_input("Choice: =>  "))
if option == 1:
    print "TODO MAPPING HEURISTIC 1"
if option == 2:
    print "TODO MAPPING HEURISTIC 2"

print "Player 2 is G and will play second"
print "would you like to use heuristic 1 or 2 for Player 2?"
option = int(raw_input("Choice: =>  "))
if option == 1:
    print "TODO MAPPING HEURISTIC 1"
if option == 2:
    print "TODO MAPPING HEURISTIC 2"



