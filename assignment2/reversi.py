import sys

USAGE_ERROR = """\
Usage: python3 reversi <player1 TYPE> <player2 TYPE>
TYPE is either human or minimax
"""

class PlayerType:
    HUMAN = 1
    ROBOT = 2

class Player:
    ONE = 1
    TWO = 2

class Square:
    PLAYER_1 = 'X'
    PLAYER_2 = 'O'
    EMPTY = '.'

def create_board(size):
    """ Creates a board, including correct starting locations.
    Will have a range error if board is smaller than 1. """
    board = [[Square.EMPTY for x in range(size)] for y in range(size)]

    mid = size // 2
    board[mid - 1][mid - 1] = Square.PLAYER_2
    board[mid][mid - 1] = Square.PLAYER_1
    board[mid - 1][mid] = Square.PLAYER_1
    board[mid][mid] = Square.PLAYER_2

    return board

def print_board(board):
    for y, column in enumerate(board):
        for x, _ in enumerate(column):
            print(str(board[x][y]) + ' ', end='')
        print()

def player_type_from_argv(i):
    # Ensure we don't go out of range
    if len(sys.argv) < i:
        sys.exit(USAGE_ERROR)

    if sys.argv[i].lower() == "human":
        return PlayerType.HUMAN
    elif sys.argv[i].lower() == "minimax":
        return PlayerType.ROBOT
    else:
        sys.exit(USAGE_ERROR)

def main():
    player1 = player_type_from_argv(1)
    player2 = player_type_from_argv(2)

    board = create_board(4)
    print_board(board)

# Prevent running if imported as a module
if __name__ == "__main__":
    main()
