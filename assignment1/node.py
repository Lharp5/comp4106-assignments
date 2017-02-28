from state import State


class Node(object):
    def __init__(self, state, goal_state=None, heuristic_function=None, parent=None):
        self.state = state
        self.parent = parent
        self.goal_state = goal_state
        # Calculate the heuristic and store its value
        self.heuristic_function = heuristic_function
        if heuristic_function is None:
            self.heuristic = 0
        else:
            self.heuristic = heuristic_function(self.state, self.goal_state)

        if parent is None:
            self.cost = 0
        else:
            self.cost = parent.cost + state.get_cost(parent.state)

    def generate_children(self):
        children = []
        states = self.state.get_child_states()
        for state in states:
            children.append(Node(state, self.goal_state, self.heuristic_function, self))
        return children
