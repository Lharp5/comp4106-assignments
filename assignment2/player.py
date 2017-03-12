from board import Board
from search import Search


class Player(object):
    def __init__(self, player, heuristic, search_depth):
        self.player = player
        self.heuristic = heuristic
        self.search = Search(search_depth, self.player)

    # TODO call the search in here and make the move
    def play(self, board):
        board_state, move = self.search.get_best_move(board, self.player, self.heuristic)
        return board_state, move
