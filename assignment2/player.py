from board import Board
from search import Search


class Player(object):
    def __init__(self, player, heuristic, search_depth):
        self.player = player
        self.heuristic = heuristic
        self.search = Search(self.player, search_depth)
        self.move_count = 0

    # TODO call the search in here and make the move
    def play(self, board):
        self.move_count += 1
        board_state, move = self.search.get_best_move(board, self.player, self.heuristic)
        print "A/B Prunned: " + str(self.search.trimmed)
        print self.player + " Makes move: "+str(move)
        return board_state
