from node import Node
from state import State
from collections import deque


class Search(object):
    def __init__(self):
        self.search ="None"

        # states already visited
        self.visited = set()
        self.queue = deque()

    def solve(self, initial_state, goal_state):
        return []


class BFS(Search):
    def __init__(self):
        Search.__init__(self)
        self.search = "BFS"

    def solve(self, initial_state, goal_state):
        root = Node(initial_state)
        current_node = root
        children = root.generate_children()

        self.visited.add(current_node.state)
        self.queue.extend(children)

        # We grab the last element, then check if its the goal or if its already been seen
        # If it has not been seen we add all its children to the end of the list.
        # We Then take the next element in the list which will progress in a breadth first manner
        while len(self.queue) > 0 and current_node.state is not goal_state:
            current_node = self.queue.popleft()
            if current_node.state in self.visited:
                continue

            if current_node.state == goal_state:
                break

            self.queue.extend([x for x in current_node.generate_children() if x.state not in self.visited])
            self.visited.add(current_node.state)

        # We have not found a solution return empty
        if current_node.state != goal_state:
            return []

        # We have found a solution so build up the path
        solution = []
        while current_node is not None:
            solution.append(current_node)
            current_node = current_node.parent

        # Put it in chronological order
        solution.reverse()

        return solution


class DFS(Search):
    def __init__(self):
        Search.__init__(self)
        self.search = "DFS"

    def solve(self, initial_state, goal_state):
        root = Node(initial_state)
        current_node = root
        children = root.generate_children()

        self.visited.add(current_node.state)
        self.queue.extend(children)

        # We grab the last element, then check if its the goal or if its already been seen
        # If it has not been seen we add all its children to the end of the list.
        # This will progress down each end path to the bottom and work up progressing a depth first manner
        while len(self.queue) > 0 and current_node.state is not goal_state:
            current_node = self.queue.pop()
            if current_node.state in self.visited:
                continue

            if current_node.state == goal_state:
                break

            self.queue.extend([x for x in current_node.generate_children() if x.state not in self.visited])
            self.visited.add(current_node.state)

        # We have not found a solution return empty
        if current_node.state != goal_state:
            return []

        # We have found a solution so build up the path
        solution = []
        while current_node is not None:
            solution.append(current_node)
            current_node = current_node.parent

        # Put it in chronological order
        solution.reverse()

        return solution


class AS(Search):
    def __init__(self):
        Search.__init__(self)
        self.search = "A*"

    def solve(self, initial_state, goal_state):
        return []
