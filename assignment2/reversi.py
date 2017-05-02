import sys

class PlayerType:
    HUMAN = 1
    MINIMAX = 2

class Square:
    PLAYER_1 = 1
    PLAYER_2 = 2
    EMPTY = 3

def create_board(size):
    return [[Square.EMPTY for x in range(size)] for y in range(size)]

def print_board(board):
    for row in board:
        for square in row:
            print(square + ' ', end='')
        print()

def main():
    usage_error = """\
Usage: reversi <player1 TYPE> <player2 TYPE>,
where TYPE is either human or minimax
"""

    if len(sys.argv) < 4:
        sys.exit(usage_error)

    board = create_board(4)
    print_board(board)

# Prevent running if imported as a module
if __name__ == "__main__":
    main()
