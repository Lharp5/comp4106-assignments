from board import Board
from copy import deepcopy
import math


class Node(object):
    def __init__(self, state, heuristic, parent=None, move=None):
        self.state = state
        self.heuristic = heuristic
        self.move = move
        self.parent = parent

    def evaluate(self, player):
        return self.heuristic(self.state, player)

    def get_children_moves(self, player):
        children = []
        for x, row in enumerate(self.state.state):
            for y, square in enumerate(row):
                # If we are not considering a square controlled by player then don't bother adding the child
                if square is None or len(square) <= 0 or square[-1] != player:
                    continue

                # if len(children) == 49:
                #     print "BLAH"

                # for 1 to number of pieces you can move, generate your moves only if valid
                # note: python range is exclusive so it would be 1-5
                for numPieces in range(1, len(square)+1):
                    # moving from 1 up to n pieces away
                    for dist in range(1, numPieces+1):
                        # moving along the positive X
                        if self.state.is_valid_move(player, (x, y, numPieces), (x + dist, y)):
                            children.append(((x, y, numPieces), (x + dist, y)))
                        # moving along the negative X
                        if self.state.is_valid_move(player, (x, y, numPieces), (x - dist, y)):
                            children.append(((x, y, numPieces), (x - dist, y)))
                        # moving along the positive y
                        if self.state.is_valid_move(player, (x, y, numPieces), (x, y + dist)):
                            children.append(((x, y, numPieces), (x, y + dist)))
                        # moving along the negative y
                        if self.state.is_valid_move(player, (x, y, numPieces), (x, y - dist)):
                            children.append(((x, y, numPieces), (x, y - dist)))

        # return the list of our children
        return children


class Search(object):
    def __init__(self, player, search_depth):
        self.depth = search_depth
        self.player = player
        self.trimmed = 0

    def get_best_move(self, current_board_state, player, heuristic):
        children_moves = Node(current_board_state, heuristic).get_children_moves(player)
        best_move = None
        best_state = None
        best_score = float('-inf')

        for move in children_moves:
            best_node = Node(current_board_state.make_move(player, move[0], move[1]),
                             heuristic,
                             parent=children_moves,
                             move=move)
            score = self.min_value(best_node, player, self.depth-1, float('-inf'), float('inf'))
            if score > best_score:
                best_score = score
                best_state = best_node.state
                best_move = best_node.move

        return best_state, best_move

    def max_value(self, node, player, depth, a, b):
        next_player = 'R' if player == 'G' else 'G'
        if depth == 0:
            return node.evaluate(self.player)

        children = node.get_children_moves(player)
        for child in children:
            a = max(a, self.min_value(Node(node.state.make_move(player, child[0], child[1]),
                                           node.heuristic,
                                           parent=node,
                                           move=child),
                                      next_player,
                                      depth-1,
                                      a,
                                      b))
            if a >= b:
                self.trimmed += 1
                return a
        return a

    def min_value(self, node, player, depth, a, b):
        next_player = 'R' if player == 'G' else 'G'
        if depth == 0:
            return node.evaluate(self.player)

        children = node.get_children_moves(player)
        for child in children:
            b = min(b, self.max_value(Node(node.state.make_move(player, child[0], child[1]), node.heuristic,
                                           parent=node,
                                           move=child),
                                      next_player,
                                      depth-1,
                                      a,
                                      b))
            if b <= a:
                self.trimmed += 1
                return b
        return b

