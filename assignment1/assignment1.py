from search import BFS, DFS, AS
from state import BridgeState, SquareState


class Problem(object):
    def __init__(self, title):
        self.search = None
        self.initial_state = None
        self.solution = None
        self.goal_state = None

        print "\n\n"
        print title
        print "================================"
        print "Enter -1 to go back a menu"
        print "\n "

    def get_initial_state(self):
        print "Override me"

    def get_search(self):
        print "================================"
        print "Choose a Search Method:"
        print "================================"
        print "1. Depth First Search"
        print "2. Breadth First Search"
        print "3. A* Heuristic Search"

        search_input = int(raw_input("Enter search choice: =>  "))

        if search_input is -1:
            return
        elif search_input is 1:
            self.search = DFS()
        elif search_input is 2:
            self.search = BFS()
        elif search_input is 3:
            self.search = AS()

    def run_search(self, heuristic=None):
        if self.goal_state is None:
            print "No Goal State Specified"
            return

        self.solution = self.search.solve(self.initial_state, self.goal_state, heuristic)
        print "================================"
        print " Result: "
        print "================================"


class BridgeProblem(Problem):
    def __init__(self):
        Problem.__init__(self, "Commodity Transportation Problem")

    def get_initial_state(self):
        people = []

        num_people = int(raw_input("Enter the Number of People Needing to cross: =>  "))

        while num_people > 0:
            people_input = int(raw_input("Enter Speed of Person: =>  "))

            if people_input is -1:
                break

            people.append(people_input)
            num_people -= 1

        self.initial_state = BridgeState(people)

    # sum the cost to transfer over the remaining
    def heuristic1(self, state, goal_state):
        # Find where the torch is calculate the value of the side we had left previously
        return sum(state.state[0])

    # sum the cost of the remaining and add the cost of walking back and forth
    def heuristic2(self, state, goal_state):
        temp_list = list(state.state[1])
        try:
            temp_list.remove(0)
        except ValueError:
            pass
        if len(temp_list) == 0:
            return 0

        return len(state.state[0]) * min(temp_list)

    # take the average of the two
    def heuristic3(self, state, goal_state):
        return (self.heuristic1(state, goal_state) + self.heuristic2(state, goal_state)) / 2

    def run_search(self, heuristic=None):
        self.goal_state = BridgeState(self.initial_state.state[1], self.initial_state.state[0])
        Problem.run_search(self, heuristic=heuristic)
        if len(self.solution) is 0:
            print "No Solution Found"
        else:
            x = 0
            print "Legend: 0 = Torch"
            for step in self.solution:
                print 'Step '+repr(x) + ': ' + repr(step.state)
                x += 1

            print "Total Time: "+repr(self.solution[-1].cost)
            print "================================"


class SquareProblem(Problem):
    def __init__(self):
        Problem.__init__(self, "Space Management Problem")

    def get_initial_state(self):

        starting_state = []
        goal_state = []

        print "reading from board.txt"
        with open("board.txt") as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            # set up the rows
            params = content.pop(0).split()
            rows = int(params[0])
            columns = int(params[1])

            for x in range(0, rows):
                starting_state.append(content.pop(0).split())

            for x in range(0, rows):
                goal_state.append(content.pop(0).split())

        self.initial_state = SquareState(rows, columns, starting_state)
        self.goal_state = SquareState(rows, columns, goal_state)

    # sum the cost to transfer over the remaining
    def heuristic1(self, state, goal_state):
        oop = 0
        for a, b in zip(state.state, goal_state.state):
            for x, y in zip(a, b):
                if x != y:
                    oop += 1
        return oop

    # sum the cost of the remaining and add the cost of walking back and forth
    def heuristic2(self, state, goal_state):
        dist = 0
        for row, i in enumerate(goal_state.state):
            for col, goal_elem in enumerate(i):
                for r, elem in enumerate(state.state):
                    try:
                        c = elem.index(goal_elem)
                    except ValueError:
                        continue

                    # Doing a fake distance calculation, to determine how far away each element is
                    dist += abs(row - r) + abs(col - c)
        return dist

    # take the average of the two
    def heuristic3(self, state, goal_state):
        return (self.heuristic1(state, goal_state) + self.heuristic2(state, goal_state)) / 2

    def run_search(self, heuristic=None):
        Problem.run_search(self, heuristic=heuristic)
        if len(self.solution) is 0:
            print "No Solution Found"
        else:
            x = 0
            print "Legend: X = Blank Space"
            for step in self.solution:
                print 'Step '+repr(x) + ':'
                for row in step.state.state:
                    print row
                x += 1

            print "Total Steps: "+repr(self.solution[-1].cost)
            print "================================"


running = True

while running:
    print "\n\n"
    print "Welcome to COMP4106 Assignment 1"
    print " By Luke Harper"

    print "Please select a problem by typing in the number below...."
    print ""
    print "1. Commodity Transportation Problem"
    print "2. Space Management Problem"
    print "-1. Exit"

    try:
        option = int(raw_input("Choice: =>  "))

        if option is -1:
            break
        if option is 1:
            problem = BridgeProblem()
        if option is 2:
            problem = SquareProblem()

        problem.get_initial_state()
        problem.get_search()
        if problem.search.search == "A*":
            print " RUNNING WITH HEURISTIC 1"
            problem.run_search(heuristic=problem.heuristic1)

            print " RUNNING WITH HEURISTIC 2"
            problem.run_search(heuristic=problem.heuristic2)

            print "Running COMBINED HEURISTIC"
            problem.run_search(heuristic=problem.heuristic3)
        else:
            problem.run_search()

    except ValueError:
        option = 0
        # pass





