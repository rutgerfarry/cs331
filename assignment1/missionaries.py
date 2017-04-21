import sys
import queue

def enum(**enums):
    return type('Enum', (), enums)

""" Simple enumeration to represent the state of the boat """
Boat = enum(LEFT=1, RIGHT=2)

class State(object):
    """Represents a state in the missionaries and cannibals problem

    Attributes:

        missionary_left (int): Number of missionaries on the left bank
        cannibal_left (int): Number of cannibals on the left bank

        missionary_right (int): Number of missionaries on the right bank
        cannibal_right (int): Number of cannibals on the right bank

        boat_location (Enum): Whether boat is on the left or right bank

    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 missionary_left, cannibal_left,
                 missionary_right, cannibal_right,
                 boat_location):
        self.missionary_left = missionary_left
        self.cannibal_left = cannibal_left
        self.missionary_right = missionary_right
        self.cannibal_right = cannibal_right

        self.boat_location = boat_location

    @staticmethod
    def from_string(data_string):
        left_bank = data_string.split("\n")[0].split(",")
        right_bank = data_string.split("\n")[1].split(",")

        missionary_left = int(left_bank[0])
        cannibal_left = int(left_bank[1])
        missionary_right = int(right_bank[0])
        cannibal_right = int(right_bank[1])

        if int(left_bank[2]) == 1:
            boat_location = Boat.LEFT
        elif int(right_bank[2]) == 1:
            boat_location = Boat.RIGHT
        else:
            raise ValueError

        return State(missionary_left, cannibal_left,
                     missionary_right, cannibal_right,
                     boat_location)

    def is_valid(self):
        return self.missionary_left >= 0 and self.missionary_right >= 0 \
                and self.cannibal_left >= 0 and self.cannibal_right >= 0 \
                and (self.missionary_left >= self.cannibal_left or self.missionary_left == 0) \
                and (self.missionary_right >= self.cannibal_right or self.missionary_right == 0)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self):
        return ("Left Bank: {} missionaries, ".format(self.missionary_left)
                + "{} cannibals, ".format(self.cannibal_left)
                + "{} boat\n".format(1 if self.boat_location == Boat.LEFT else 0)
                + "Right Bank: {} missionaries, ".format(self.missionary_right)
                + "{} cannibals, ".format(self.cannibal_right)
                + "{} boat\n".format(1 if self.boat_location == Boat.RIGHT else 0))

class Node(object):
    def __init__(self, state, parent, action, cost=0):
        self.parent = parent
        self.state = state
        self.action = action
        self.cost = cost

    def __repr__(self):
        return str(self.state)

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.cost == other.cost
        return False

    def __hash__(self):
        return self.state.__hash__()

# Takes a state and returns the set of possible successor states
def child_nodes(node):
    state = node.state
    successors_set = set()

    if state.boat_location == Boat.LEFT:
        # Put one missionary in the boat
        successor = State(state.missionary_left - 1, state.cannibal_left,
                          state.missionary_right + 1, state.cannibal_right, Boat.RIGHT)
        if successor.is_valid():
            successors_set.add(Node(successor,
                                    node,
                                    "put one missionary in the boat"))
        # Put two missionaries in the boat
        successor = State(state.missionary_left - 2, state.cannibal_left,
                          state.missionary_right + 2, state.cannibal_right, Boat.RIGHT)
        if successor.is_valid():
            successors_set.add(Node(successor,
                                    node,
                                    "put two missionaries in the boat"))
        # Put one cannibal in the boat
        successor = State(state.missionary_left, state.cannibal_left - 1,
                          state.missionary_right, state.cannibal_right + 1, Boat.RIGHT)
        if successor.is_valid():
            successors_set.add(Node(successor,
                                    node,
                                    "put one cannibal in the boat"))
        # Put one cannibal and one missionary in the boat
        successor = State(state.missionary_left - 1, state.cannibal_left - 1,
                          state.missionary_right + 1, state.cannibal_right + 1, Boat.RIGHT)
        if successor.is_valid():
            successors_set.add(Node(successor,
                                    node,
                                    "put one cannibal one missionary in the boat"))
        # Put two cannibals in the boat
        successor = State(state.missionary_left, state.cannibal_left - 2,
                          state.missionary_right, state.cannibal_right + 2, Boat.RIGHT)
        if successor.is_valid():
            successors_set.add(Node(successor,
                                    node,
                                    "put two cannibals in the boat"))

    elif state.boat_location == Boat.RIGHT:
        # Put one missionary in the boat
        successor = State(state.missionary_left + 1, state.cannibal_left,
                          state.missionary_right - 1, state.cannibal_right, Boat.LEFT)
        if successor.is_valid():
            successors_set.add(Node(successor,
                                    node,
                                    "put one missionary in the boat"))
        # Put two missionaries in the boat
        successor = State(state.missionary_left + 2, state.cannibal_left,
                          state.missionary_right - 2, state.cannibal_right, Boat.LEFT)
        if successor.is_valid():
            successors_set.add(Node(successor,
                                    node,
                                    "put two missionaries in the boat"))
        # Put one cannibal in the boat
        successor = State(state.missionary_left, state.cannibal_left + 1,
                          state.missionary_right, state.cannibal_right - 1, Boat.LEFT)
        if successor.is_valid():
            successors_set.add(Node(successor,
                                    node,
                                    "put one cannibal in the boat"))
        # Put one cannibal and one missionary in the boat
        successor = State(state.missionary_left + 1, state.cannibal_left + 1,
                          state.missionary_right - 1, state.cannibal_right - 1, Boat.LEFT)
        if successor.is_valid():
            successors_set.add(Node(successor,
                                    node,
                                    "put one cannibal one missionary in the boat"))
        # Put two cannibals in the boat
        successor = State(state.missionary_left, state.cannibal_left + 2,
                          state.missionary_right, state.cannibal_right - 2, Boat.LEFT)
        if successor.is_valid():
            successors_set.add(Node(successor,
                                    node,
                                    "put two cannibals in the boat"))

    return successors_set

def bfs(begin_state, goal_state):
    if begin_state == goal_state:
        return True

    frontier = queue.Queue()
    frontier.put(Node(begin_state, None, None))
    explored = set()

    while True:
        if frontier.empty():
            return False

        node = frontier.get()
        explored.add(node)
        children = child_nodes(node)
        for child in children:
            if child not in explored or child not in frontier:
                if goal_state == child.state:
                    print_actions(child)
                    return True
                frontier.put(child)

def dfs(begin_state, goal_state):
    if begin_state == goal_state:
        return True

    frontier = queue.LifoQueue()
    frontier.put(Node(begin_state, None, None))
    explored = set()

    while True:
        if frontier.empty():
            return False

        node = frontier.get()
        explored.add(node)
        children = child_nodes(node)
        for child in children:
            if child not in explored or child not in frontier:
                if goal_state == child.state:
                    print_actions(child)
                    return True
                frontier.put(child)

def depth_limited_search(begin_state, goal_state, limit):
    start_node = Node(begin_state, None, None)
    return recursive_dls(start_node, goal_state, limit)

def recursive_dls(node, goal_state, limit):
    if node.state == goal_state:
        return True
    elif limit == 0:
        return "cutoff"
    else:
        cutoff_occurred = False
        for child in child_nodes(node):
            result = recursive_dls(child, goal_state, limit - 1)
            if result == "cutoff":
                cutoff_occurred = True
            elif result == True:
                print_actions(child)
                return True
        if cutoff_occurred:
            return "cutoff"
        else:
            return False

def iterative_deepening_search(begin_state, goal_state):
    for depth in range(sys.maxsize**10):
        result = depth_limited_search(begin_state, goal_state, depth)
        if result != "cutoff":
            return result

# Lower score is closer to solution
def score(current_state, goal_state):
    return ((goal_state.missionary_left - current_state.missionary_left) +
            (goal_state.cannibal_left - current_state.cannibal_left))

def a_star(begin_state, goal_state):
    if begin_state == goal_state:
        return True
    begin_node = Node(begin_state, None, None)
    frontier = queue.PriorityQueue()
    frontier.put((score(begin_node.state, goal_state), begin_node))
    explored = set()

    while frontier:
        node = frontier.get()[1]
        explored.add(node)
        for child in child_nodes(node):
            if child not in explored:
                if goal_state == child.state:
                    print_actions(child)
                    return True
                frontier.put((score(child.state, goal_state), child))

def print_actions(node):
    while node != None:
        print(node.action)
        print(node.state)
        node = node.parent

def main():
    if len(sys.argv) == 4:
        begin_state = State.from_string(open(sys.argv[1]).read())
        goal_state = State.from_string(open(sys.argv[2]).read())

    a_star(begin_state, goal_state)

# Prevent running if imported as a module
if __name__ == "__main__":
    main()
