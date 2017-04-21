import sys
import queue
from enum import Enum

class Boat(Enum):
    """ Simple enumeration to represent the state of the boat """
    LEFT = True
    RIGHT = False

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
    def __init__(self, state, parent, action):
        self.parent = parent
        self.state = state
        self.action = action

    def __repr__(self):
        return str(self.state)

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

def print_actions(node):
    while node != None:
        print(node.action)
        print(node.state)
        node = node.parent

def main():
    if len(sys.argv) == 4:
        begin_state = State.from_string(open(sys.argv[1]).read())
        goal_state = State.from_string(open(sys.argv[2]).read())

        bfs(begin_state, goal_state)

# Prevent running if imported as a module
if __name__ == "__main__":
    main()
