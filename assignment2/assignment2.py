from board import Board
from player import Player

sample_start = [[None, None,    [],    [],    [],    [],    None,    None],
                [None, ['R'],   ['R'], ['G'], ['G'], ['R'], ['R'],   None],
                [[],   ['G'],   ['G'], ['R'], ['R'], ['G'], ['G'],   []],
                [[],   ['R'],   ['R'], ['G'], ['G'], ['R'], ['R'],   []],
                [[],   ['G'],   ['G'], ['R'], ['R'], ['G'], ['G'],   []],
                [[],   ['R'],   ['R'], ['G'], ['G'], ['R'], ['R'],   []],
                [None, ['G'],   ['G'], ['R'], ['R'], ['G'], ['G'],   None],
                [None, None,    [],    [],    [],    [],    None,    None]]

print "Starting Computer vs Computer Game"


def count_stacks_h(state, player):
    controlled = 0
    for row in state:
        for square in row:
            if square is not None:
                if len(square) > 0 and square[-1] == player:
                    controlled += 1

    return controlled


def heuristic1(state, player):
    score = 0

    for row in state.state:
        for square in row:
            if square is not None:
                if len(square) > 0:
                    if square[-1] != player:
                        score -= 1

    return score


def heuristic2(state, player):
    mine = 0
    enemy = 0

    enemy_player = 'R' if player == 'G' else 'R'

    for row in state.state:
        for square in row:
            if square is not None:
                if len(square) > 0:
                    if square[-1] == player:
                        mine += 1
                    else:
                        enemy += 1

    return (mine - enemy) + (state.bank[player][enemy_player] - state.bank[enemy_player][player])


print "Enter the AI Search Depth"
depth = int(raw_input("Choice: =>  "))


print "Player 1 is R and will play first"
print "Would you like to use heuristic 1 or 2 for Player 1?"
option = int(raw_input("Choice: =>  "))

p1H = None
if option == 1:
    p1H = heuristic1
if option == 2:
    p1H = heuristic2

player1 = Player('R', p1H, depth)

print "Player 2 is G and will play second"
print "would you like to use heuristic 1 or 2 for Player 2?"
p2H = None
option = int(raw_input("Choice: =>  "))
if option == 1:
    p2H = heuristic1
if option == 2:
    p2H = heuristic2

player2 = Player('G', p2H, depth)

print "======================"
print "Starting Game"
print "======================"
current_state = Board(sample_start)
valid_moves = True
current_player = player1

while valid_moves:
    print current_state
    pieces_commanded = count_stacks_h(current_state.state, current_player.player)
    if pieces_commanded == 0:
        print current_player.player + " Has Lost!"
        break

    current_state = current_player.play(current_state)
    print current_player.player + " move: " + str(current_player.move_count)
    current_player = player1 if current_player == player2 else player2
