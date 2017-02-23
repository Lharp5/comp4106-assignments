from search import BFS, DFS, AS, Search
from node import Node
from state import BridgeState


class Problem(object):
    def __init__(self, title):
        self.search = None
        self.initial_state = None

        print "\n\n"
        print title
        print "================================"
        print "Enter -1 to go back a menu"
        print "\n "

    def get_initial_state(self):
        print "Override me"

    def get_search(self):
        # TODO: Gather the type of search they wish to run
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

    def run_search(self):
        goal_state = BridgeState(self.initial_state.state[1], self.initial_state.state[0])
        solution = self.search.solve(self.initial_state, goal_state)

        print "================================"
        print " Result: "
        print "================================"

        if len(solution) is 0:
            print "No Solution Found"
        else:
            x = 0
            print "Legend: 0 = Torch"
            for step in solution:
                print 'Step '+repr(x) + ': ' + repr(step.state)
                x += 1

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


class SquareProblem(Problem):
    def __init__(self):
        Problem.__init__(self, "Space Management Problem")

    def get_initial_state(self):
        print "square Initial State"


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
        problem.run_search()


    except ValueError:
        option = 0
        # pass





