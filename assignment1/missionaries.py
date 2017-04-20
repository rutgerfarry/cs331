import sys
from state import State

class Node(object):
    def __init__(self, state, parent, action):
        self.parent = parent
        self.state = state
        self.action = action

    def __repr__(self):
        return String(self.state)

# Takes a state and returns the set of possible actions
def actions(state):
    return

# Prevent running if imported as a module
if __name__ == "__main__":
    if len(sys.argv) == 4:
        begin_state = State.from_string(open(sys.argv[1]).read())
        final_state = State.from_string(open(sys.argv[2]).read())

        explored_set = set()

        print "begin state:::::::::::::::::::::::::::"
        print begin_state

        print "final state:::::::::::::::::::::::::::"
        print final_state

