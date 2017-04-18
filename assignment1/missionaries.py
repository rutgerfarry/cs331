import sys
from state import State

# Prevent running if imported as a module
if __name__ == "__main__":
    if len(sys.argv) == 4:
        begin_state = State(open(sys.argv[1]).read())
        final_state = State(open(sys.argv[2]).read())

        print "begin state:::::::::::::::::::::::::::"
        print begin_state

        print "final state:::::::::::::::::::::::::::"
        print final_state
