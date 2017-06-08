import sys
import math

USAGE_ERROR = """\
Usage: python3 reversi <player1 TYPE> <player2 TYPE>
TYPE is either human or minimax
"""

class IllegalMoveError(Exception):
    def __init__(self, player, i, board):
        super().__init__()
        self.player = player
        self.x = index_as_tuple(i, board)[0]
        self.y = index_as_tuple(i, board)[1]
        self.board = board

    def __str__(self):
        print_board(self.board)
        return "{} cannot move to square ({}, {})".format(self.player,
                                                          chr(self.x + 65),
                                                          self.y)

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
    board = dangerously_make_move(Player.TWO, mid - 1, mid - 1, board)
    board = dangerously_make_move(Player.ONE, mid, mid - 1, board)
    board = dangerously_make_move(Player.ONE, mid - 1, mid, board)
    board = dangerously_make_move(Player.TWO, mid, mid, board)

    return board

# Helper functions

def opponent(player):
    return Player.ONE if player is Player.TWO else Player.TWO

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
    """ Returns size of one side of the board """
    return int(math.sqrt(len(board)))

def index_as_tuple(i, board):
    """ Takes an index and returns as a board position in form of (x,y) """
    size = board_size(board)
    return (i % size,
            i // size)

def tuple_as_index(t, board):
    """ Takes a board position in the form of (x,y) and returns an index """
    size = board_size(board)
    return t[0] + t[1] * size

# Move-related functions

def find_bracket(i, player, delta, board):
    """" Returns the valid move for a player from index i
    in the given direction (delta) """

    # print("i: {}, player: {}, delta: {}".format(i, player, delta))

    start = i
    is_valid = lambda i: 0 <= i < len(board)

    while is_valid(i + delta) and board[i + delta] == opponent(player):
        i += delta

    if i != start:
        if is_valid(i + delta) and board[i + delta] == EMPTY_SQUARE:
            return i + delta

def deltas(board):
    size = board_size(board)

    up, down, left, right = -size, size, -1, +1
    up_left, up_right, down_left, down_right = -size-1, -size+1, size-1, size+1
    return (up, down, left, right, up_right, up_left, down_right, down_left)

def valid_moves(player, board):
    """ Returns the set of valid moves for the given player.
    Moves are tuples in the form of (x,y), e.g. (1,3) """

    moves = set()
    positions = {i for i, piece in enumerate(board) if piece == player}

    for p in positions:
        moves_for_p = {find_bracket(p, player, d, board) for d in deltas(board)}
        moves = moves.union(moves_for_p)

    return moves

def make_flips(i, player, delta, board):
    positions = {i for i, piece in enumerate(board) if piece == player}
    for p in positions:
        if find_bracket(p, player, delta, board) == i:
            while p != i:
                board[p+delta] = player
                p += delta

    return board

def make_move(player, x, y, board):
    """ User-facing move function with validation. """

    board = list(board)

    i = tuple_as_index((x, y), board)
    if i in valid_moves(player, board):
        for d in deltas(board):
            board = make_flips(i, player, d, board)
    else:
        raise IllegalMoveError(player, i, board)

    return board

def dangerously_make_move(player, x, y, board):
    """ Moves without validation or flips. For internal setup use only. """

    i = tuple_as_index((x, y), board)
    board[i] = player
    return board

def player_score(player, board):
    return len([piece for piece in board if piece == player])

# Strategies

def human_strategy(player, board):
    raw_move = input("Enter your move (example A1): ")
    x = raw_move[0:1]
    y = raw_move[1:]

    if not x.isalpha():
        print("{} is an invalid column, try again.".format(x))
        return human_strategy(player, board)
    if not y.isdigit():
        print("{} is an invalid row, try again.".format(y))
        return human_strategy(player, board)

    x = ord(x.upper()) - 65
    y = int(y)

    try:
        board = make_move(player, x, y, board)
        return board

    except IllegalMoveError:
        print("{} is not a legal move!".format(raw_move))
        print("Possible moves are: {}".format(valid_moves(player, board)))
        print("Try again.")

    return human_strategy(player, board)

# Minimax

def minimax(player, board, depth):
    moves = valid_moves(player, board)
    def value(board):
        return -minimax(opponent(player), board, depth - 1)[0]

    if depth == 0:
        return player_score(player, board), None

    if moves == {None}:
        return player_score(player, board), None

    moves.remove(None)

    return max((value(make_move(player,
                                index_as_tuple(m, board)[0],
                                index_as_tuple(m, board)[1],
                                board)), m) for m in moves)

def minimax_strategy(player, board):
    move = minimax(player, board, 4)
    board = make_move(board, move[0], move[1], board)
    return board

def player_strategy_from_argv(i):
    """ Parses argv at the given index and returns strategy for user """

    # Ensure we don't look out of range
    if len(sys.argv) < i:
        sys.exit(USAGE_ERROR)

    if sys.argv[i].lower() == "human":
        return human_strategy
    elif sys.argv[i].lower() == "minimax":
        return minimax_strategy
    else:
        sys.exit(USAGE_ERROR)

# Main

def main():
    player1_strat = player_strategy_from_argv(1)
    player2_strat = player_strategy_from_argv(2)

    strategy = lambda p: player1_strat if p == Player.ONE else player2_strat

    current_player = Player.ONE

    board = create_board(4)

    while valid_moves(current_player, board) != {None}:
        print()
        print("Player 1 score: {}".format(player_score(Player.ONE, board)))
        print("Player 2 score: {}".format(player_score(Player.TWO, board)))
        print_board(board)
        print("Player {}'s turn:".format(current_player))
        print(minimax(current_player, board, 1))
        board = strategy(current_player)(current_player, board)
        current_player = opponent(current_player)

    print_board(board)
    print("No more moves are possible, game over!")

# Prevent running if imported as a module
if __name__ == "__main__":
    main()
