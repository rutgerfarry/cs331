import sys
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
        return "{},{},{}\n{},{},{}".format(
            self.missionary_left,
            self.cannibal_left,
            1 if self.boat_location == Boat.LEFT else 0,
            self.missionary_right,
            self.cannibal_right,
            1 if self.boat_location == Boat.RIGHT else 0)

class Node(object):
    def __init__(self, state, parent, action):
        self.parent = parent
        self.state = state
        self.action = action

    def __repr__(self):
        return str(self.state)

# Takes a state and returns the set of possible actions
def actions(state):
    action_set = set()
    return

def main():
    if len(sys.argv) == 4:
        begin_state = State.from_string(open(sys.argv[1]).read())
        final_state = State.from_string(open(sys.argv[2]).read())

        explored_set = set()

        print("begin state:::::::::::::::::::::::::::")
        print(begin_state)

        print("final state:::::::::::::::::::::::::::")
        print(final_state)

# Prevent running if imported as a module
if __name__ == "__main__":
    main()
