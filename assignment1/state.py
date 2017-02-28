from copy import deepcopy
from itertools import combinations
from collections import Counter


class State(object):
    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return repr(self.state)

    def __init__(self, state=None):
        self.state = state

    def get_cost(self, parent_state):
        return 1

    def get_child_states(self):
        return []

    def __hash__(self):
        return hash(repr(self.state))

    def __eq__(self, other):
        return self.state == other.state

    def __ne__(self, other):
        return self.state != other.state


class BridgeState(State):
    def __init__(self, state_left=None, state_right=None):
        if state_right is None:
            state_left.insert(0, 0)
            new_state = [sorted(state_left), []]
        else:
            new_state = [sorted(state_left), sorted(state_right)]
        State.__init__(self, new_state)

    def __eq__(self, other):
        return self.state[0] == other.state[0] and self.state[1] == other.state[1]

    def __ne__(self, other):
        return self.state[0] != other.state[0] or self.state[1] != other.state[1]

    def __repr__(self):
        return repr(self.state)

    def get_cost(self, parent_state):
        if 0 in self.state[0]:
            source = 1
            dest = 0
        else:
            source = 0
            dest = 1

        moved_entries = Counter(self.state[dest]) & Counter(parent_state.state[source])
        return max(list(moved_entries.elements()))

    def get_child_states(self):
        take_from = 0
        put_into = 1

        if 0 in self.state[1]:
            take_from = put_into
            put_into = 0

        # Taking our torch out of one side
        temp = deepcopy(self.state)
        temp[take_from].remove(0)

        child_states = []

        # Moving only 1 person
        for element in temp[take_from]:
            temp2 = deepcopy(temp)
            temp2[take_from].remove(element)
            temp2[put_into].append(element)
            # putting the torch back on the other side
            temp2[put_into].insert(0, 0)
            child_states.append(BridgeState(temp2[0], temp2[1]))

        # Moving 2 people
        for pair in combinations(temp[take_from], 2):
            temp2 = deepcopy(temp)
            temp2[take_from].remove(pair[0])
            temp2[put_into].append(pair[0])
            temp2[take_from].remove(pair[1])
            temp2[put_into].append(pair[1])
            # Putting the torch back on the other side
            temp2[put_into].insert(0, 0)
            child_states.append(BridgeState(temp2[0], temp2[1]))
        return child_states


class SquareState(State):
    def __init__(self, rows, columns, state):
        self.rows = rows
        self.columns = columns
        State.__init__(self, state)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def swap(self, source_row, source_column, dest_row, dest_column):
        temp_list = deepcopy(self.state)
        temp = temp_list[source_row][source_column]
        temp_list[source_row][source_column] = temp_list[dest_row][dest_column]
        temp_list[dest_row][dest_column] = temp
        return SquareState(self.rows, self.columns, temp_list)

    def horse_jump(self, source_row, source_column, dest_row, dest_column):
        if self.state[dest_row][dest_column] is not 'X':
            value = (self.state[dest_row][dest_column], self.state[source_row][source_column]) \
                if self.state[dest_row][dest_column] > self.state[source_row][source_column] \
                else (self.state[source_row][source_column], self.state[dest_row][dest_column])
            return value
        else:
            return None

    def get_child_states(self):
        row = -1
        column = -1
        child_states = []
        jumped = set()
        for r, i in enumerate(self.state):
                for c, j in enumerate(i):
                    if j == 'X':
                        row = r
                        column = c
                        continue
                    # Down and Left/Right
                    if r < self.rows-2:
                        if c < self.columns - 1:
                            value = self.horse_jump(r, c, r+2, c + 1)
                            if value is not None and value not in jumped:
                                jumped.add(value)
                                child_states.append(self.swap(r, c, r+2, c + 1))
                        if c > 0:
                            value = self.horse_jump(r, c, r + 2, c - 1)
                            if value is not None and value not in jumped:
                                jumped.add(value)
                                child_states.append(self.swap(r, c, r + 2, c - 1))
                    # Up and Left/Right
                    if r > 1:
                        if c < self.columns - 1:
                            value = self.horse_jump(r, c, r - 2, c + 1)
                            if value is not None and value not in jumped:
                                jumped.add(value)
                                child_states.append(self.swap(r, c, r - 2, c + 1))
                        if c > 0:
                            value = self.horse_jump(r, c, r - 2, c - 1)
                            if value is not None and value not in jumped:
                                jumped.add(value)
                                child_states.append(self.swap(r, c, r - 2, c - 1))
                    # Left and Up/Down
                    if c < self.columns - 2:
                        if r < self.rows - 1:
                            value = self.horse_jump(r, c, r + 1, c + 2)
                            if value is not None and value not in jumped:
                                jumped.add(value)
                                child_states.append(self.swap(r, c, r + 1, c + 2))
                        if r > 0:
                            value = self.horse_jump(r, c, r - 1, c + 2)
                            if value is not None and value not in jumped:
                                jumped.add(value)
                                child_states.append(self.swap(r, c, r - 1, c + 2))
                    # Right and Up/Down
                    if c > 1:
                        if r < self.rows - 1:
                            value = self.horse_jump(r, c, r + 1, c - 2)
                            if value is not None and value not in jumped:
                                jumped.add(value)
                                child_states.append(self.swap(r, c, r + 1, c - 2))
                        if r > 0:
                            value = self.horse_jump(r, c, r - 1, c - 2)
                            if value is not None and value not in jumped:
                                jumped.add(value)
                                child_states.append(self.swap(r, c, r - 1, c - 2))

        if row is -1 or column is -1:
            return []

        # Swapping with blank space
        if row < self.rows -1:
            child_states.append(self.swap(row, column, row+1, column))

            if column < self.columns -1:
                child_states.append(self.swap(row, column, row + 1, column + 1))

            if column > 0:
                child_states.append(self.swap(row, column, row + 1, column - 1))

        if row > 0:
            child_states.append(self.swap(row, column, row - 1, column))
            if column < self.columns - 1:
                child_states.append(self.swap(row, column, row - 1, column + 1))

            if column > 0:
                child_states.append(self.swap(row, column, row - 1, column - 1))

        if column < self.columns - 1:
            child_states.append(self.swap(row, column, row, column + 1))

        if column > 0:
            child_states.append(self.swap(row, column, row, column - 1))

        return child_states
