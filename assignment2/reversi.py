import sys
import math

USAGE_ERROR = """\
Usage: python3 reversi <player1 TYPE> <player2 TYPE>
TYPE is either human or minimax
"""

class PlayerType:
    HUMAN = 1
    ROBOT = 2

class Player:
    ONE = 'X'
    TWO = 'O'

EMPTY_SQUARE = '.'

def create_board(size):
    """ Creates a board, including correct starting locations.
    Will have a range error if size is smaller than 2. """

    board = [EMPTY_SQUARE for x in range(size**2)]

    mid = board_size(board) // 2
    board = move(Player.TWO, mid - 1, mid - 1, board)
    board = move(Player.ONE, mid, mid - 1, board)
    board = move(Player.ONE, mid - 1, mid, board)
    board = move(Player.TWO, mid, mid, board)

    return board

def print_board(board):
    size = board_size(board)
    # Print letters for each column
    print('     ', end='')
    print(' '.join([chr(i + 65) for i in range(0, size)]))
    print('    ' + '_' + '__' * size)

    # Print numbers for row followed by board pieces
    for y in range(0, len(board), size):
        print(str(int(y / size)) + '  | ', end='')
        print(' '.join(board[y : y + size]))

def board_size(board):
    return int(math.sqrt(len(board)))

def move(player, x, y, board):
    # Allow x to be either an int or str
    if isinstance(x, str):
        x = ord(x.upper()) - 65

    size = board_size(board)
    i = x * size + y
    board[i] = player
    return board

def player_type_from_argv(i):
    """ Parses argv at the given index and returns whether user
    has selected to play against a human or robot """

    # Ensure we don't look out of range
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
