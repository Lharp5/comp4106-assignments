from copy import deepcopy
from itertools import combinations


class State(object):
    def __str__(self):
        return str(self.state)

    def __init__(self, state=None):
        self.state = state

    def get_child_states(self):
        return []

    def __hash__(self):
        return hash(repr([self.state]))

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
