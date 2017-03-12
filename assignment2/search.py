from board import Board
from copy import deepcopy
import math


class Node(object):
    def __init__(self, state, heuristic, parent=None, move=None):
        self.state = state
        self.heuristic = heuristic
        self.move = move
        self.parent = parent
        self.value = None

    def set_value(self, val):
        self.value = val

    def evaluate(self, player):
        self.value = self.heuristic(player)

    def get_children(self, player):
        children = []
        for x, row in enumerate(self.state):
            for y, square in enumerate(row):
                # If we are not considering a square controlled by player then don't bother adding the child
                if len(square) <= 0 or square[-1] != player:
                    continue

                # for 1 to number of pieces you can move, generate your moves
                # note: python range is exclusive so it would be 1-5
                for numPieces in range(1, len(square)+1):
                    # moving from 1 up to n pieces away
                    for dist in range(1, numPieces):
                        # moving along the positive X
                        new_move = self.state.make_move(player, (x, y, numPieces), (x + dist, y))
                        if new_move is not None:  # If the move was valid add it to the children list
                            children.append(Node(new_move, self.heuristic, parent=self,
                                                 move=((x, y, numPieces), (x + dist, y))))
                        # moving along the negative X
                        new_move = self.state.make_move(player, (x, y, numPieces), (x - dist, y))
                        if new_move is not None:  # If the move was valid add it to the children list
                            children.append(Node(new_move, self.heuristic, parent=self,
                                                 move=((x, y, numPieces), (x - dist, y))))
                        # moving along the positive y
                        new_move = self.state.make_move(player, (x, y, numPieces), (x, y + dist))
                        if new_move is not None:  # If the move was valid add it to the children list
                            children.append(Node(new_move, self.heuristic, parent=self,
                                                 move=((x, y, numPieces), (x, y + dist))))
                        # moving along the negative y
                        new_move = self.state.make_move(player, (x, y, numPieces), (x, y - dist))
                        if new_move is not None:  # If the move was valid add it to the children list
                            children.append(Node(new_move, self.heuristic, parent=self,
                                                 move=((x, y, numPieces), (x, y - dist))))

        # return the list of our children
        return children


class Search(object):
    def __init__(self, player, search_depth):
        self.depth = search_depth
        self.player = player

    def get_best_move(self, current_board_state, player, heuristic):
        best_node = self.alphabeta(Node(current_board_state, heuristic), self.depth, float('-inf'), float('+inf'), True, player)
        return best_node.state, best_node.move

    def alphabeta(self, node, depth, a, b, max_player, player):
        next_player = 'R' if player == 'G' else 'G'
        if depth == 0:
            node.evaluate(self.player)
            return node

        candidate = None

        if max_player:
            v = float('-inf')

            for child in node.get_children(player):
                updated_child = self.alphabeta(child, depth-1, a, b, False, next_player)
                v = max(v, updated_child.value)
                a = max(a, v)
                # Beta cutoff
                if b <= a:
                    break

                # We want to consider this node as valid if it passes the cutoff
                candidate = child
                candidate.set_value(v)
        else:
            v = float('inf')
            for child in node.get_children(player):
                updated_child = self.alphabeta(child, depth - 1, a, b, False, next_player)
                v = min(v, updated_child.value)
                b = min(b, v)
                # Alpha cut off
                if b <= a:
                    break

                # We want to consider this node as valid if it passes the cutoff
                candidate = child
                candidate.set_value(v)

        return candidate
