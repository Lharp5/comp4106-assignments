from copy import deepcopy
from itertools import combinations

board_start = [[None, None, [], [], [], [], None, None],
               [None, [],   [], [], [], [], [],   None],
               [[],   [],   [], [], [], [], [],   []],
               [[],   [],   [], [], [], [], [],   []],
               [[],   [],   [], [], [], [], [],   []],
               [[],   [],   [], [], [], [], [],   []],
               [None, [],   [], [], [], [], [],   None],
               [None, None, [], [], [], [], None, None]]


class Board(object):
    def __init__(self, board=None, bank=None):
        if board is None:
            self.state = deepcopy(board_start)
        else:
            self.state = board

        if bank is None:
            self.bank = {'R': {'R': 0, 'G': 0}, 'G': {'R': 0, 'G': 0}}
        else:
            self.bank = bank

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __str__(self):
        rep = ""
        for row in self.state:
            r = ""
            for place in row:
                entry = ""
                if place is not None:

                    if len(place) > 0:
                        entry += place[-1]
                    else:
                        entry += "E"
                    entry += repr(len(place))
                else:
                    entry = "  "
                r += entry + " "
            rep += r + "\n"

        return rep

    def __repr__(self):
        rep = []
        for row in self.state:
            r = []
            for place in row:
                entry = ""
                if place is not None:

                    if len(place) > 0:
                        entry += place[-1]
                    else:
                        entry += "E"
                    entry += repr(len(place))
                else:
                    entry = None
                r.append(entry)
            rep.append(r)

        return repr(rep)

    def capture_pieces(self, player, pieces):
        for piece in pieces:
            self.bank[player][piece] += 1

    def is_valid_move(self, player, start, dest):
        # Checking to make sure start point is in bounds
        if start[0] < 0 or start[1] < 0 or start[0] >= len(self.state) or start[1] >= len(self.state):
            return False

        # Checking to make sure dest point is in bounds
        if dest[0] < 0 or dest[1] < 0 or dest[0] >= len(self.state) or dest[1] >= len(self.state):
            return False

        # Checking to make sure we are looking at one axis
        if not ((start[0] == dest[0] and start[1] != dest[1]) or (start[0] != dest[0] and start[1] == dest[1])):
            return False

        # Checking to make sure we are not moving to a corner piece
        if dest in [(1, 0), (0, 0), (0, 1), (0, 6), (0, 7), (1, 7), (6, 7), (7, 7), (7, 6), (7, 1), (7, 0), (6, 0)]:
            return False

        # Checking to make sure we have a destination and start point
        if self.state[start[0]][start[1]] is None or self.state[dest[0]][dest[1]] is None:
            return False

        # Checking to make sure we are grabbing a valid number of pieces, and we have enough pieces
        if start[2] < 1 or start[2] > 5 or start[2] > len(self.state[start[0]][start[1]]):
            return False

        # Checking to make sure the piece we are grabbing is a player controlled square
        if self.state[start[0]][start[1]][-1] != player:
            return False

        # if we have passed all conditions we can return true
        return True

    # Attempt to make a move, returns the board state if move is valid, None otherwise
    # in: Character representing red or green player
    # in: start tuple of the x, y, n coordinate of the stack you wish to move, and number you wish to move
    # in: dest tuple of x, y coordinate of the location you wish to move to
    def make_move(self, player, start, dest):

        if not self.is_valid_move(player, start, dest):
            return None

        # Check if we are moving the correct distance away
        dist = 100  # Default large value for the if statement later
        if start[0] == dest[0] and start[1] != dest[1]:
            dist = start[1] - dest[1]
        elif start[0] != dest[0] and start[1] == dest[1]:
            dist = start[0] - dest[0]

        # Check to make sure we are not wanting to move farther then the pieces we want to grab
        if abs(dist) > start[2]:
            return None

        # Can finally attempt the move, Copying the board state to return
        new_board = Board(board=self.state, bank=self.bank)
        #  performing a python slice from the last N pieces
        temp = new_board.state[start[0]][start[1]][-start[2]:]

        # Removing those pieces from the state
        del new_board.state[start[0]][start[1]][-start[2]:]

        # Add it to our destination
        new_board.state[dest[0]][dest[1]].extend(temp)

        # if the new position has more then 5 pieces then capture the pieces
        if len(new_board.state[dest[0]][dest[1]]) > 5:
            captured = new_board.state[dest[0]][dest[1]][:5]
            del new_board.state[dest[0]][dest[1]][:5]
            new_board.capture_pieces(player, captured)

        return new_board
