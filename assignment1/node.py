from state import State


class Node(object):
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

    def generate_children(self):
        children = []
        states = self.state.get_child_states()
        for state in states:
            children.append(Node(state, self))
        return children
