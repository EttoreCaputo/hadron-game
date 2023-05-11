from hadron.board import Board
from hadron.game import Game


#    ██╗  ██╗ █████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗     ██████╗  █████╗ ███╗   ███╗███████╗
#    ██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗████╗  ██║    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
#    ███████║███████║██║  ██║██████╔╝██║   ██║██╔██╗ ██║    ██║  ███╗███████║██╔████╔██║█████╗
#    ██╔══██║██╔══██║██║  ██║██╔══██╗██║   ██║██║╚██╗██║    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝
#    ██║  ██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║ ╚████║    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
#    ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
class HadronGame(Game):
    def __init__(self, height=5, width=5):
        self.initial = Board(width=width, height=height, to_move='R', utility=0)
        self.cells = {(x, y) for y in range(width) for x in range(height)}
        self.graphic_module = None

    def actions(self, board):
        return self.valid_moves(board)

    def result(self, board, move):
        player = board.to_move
        board = board.new({move: player}, to_move=('R' if player == 'B' else 'B'))
        win = self.check_winner(board)
        board.utility = (0 if not win else +1 if player == 'R' else -1)
        return board

    def utility(self, board, player):
        return board.utility if player == 'R' else -board.utility

    def is_terminal(self, board):
        return board.utility != 0

    def neighbors(self, board: Board, row, col):
        neighbors = 0
        if (row - 1, col) in board:
            neighbors += ord(board[row - 1, col])
        if (row, col - 1) in board:
            neighbors += ord(board[row, col - 1])
        if (row, col + 1) in board:
            neighbors += ord(board[row, col + 1])
        if (row + 1, col) in board:
            neighbors += ord(board[row + 1, col])
        return neighbors

    def is_a_valid_action(self, board: Board, row, col):
        # This is an optimized version of the function to check if a move is valid
        # You can check a valid move by checking if the sum of the red neighbors is the same as the sum of the blue.

        # This version is based on the following observations:
        # The ascii code of 'R' is 82, the ascii code of 'B' is 66 and the ascii code of '.' is 46
        # 92 -> 2 * '.', case: corner
        # 138 -> 3 * '.', case: edge
        # 184 -> 4 * '.', case: no neighbors
        # 148 -> 1 * 'R' + 1 * 'B', case: corner
        # 194 -> 1 * 'R' + 1 * 'B' + 1 * '.', case: edge
        # 240 -> 1 * 'R' + 1 * 'B' + 2 * '.'
        # 296 -> 2 * 'R' + 2 * 'B'
        if board[row, col] == board.empty:
            value = self.neighbors(board, row, col)
            return value == 92 or value == 138 or value == 184 \
                or value == 148 or value == 194 or value == 240 \
                or value == 296 \
                or value == 0
        return False

    def valid_moves(self, board: Board) -> list[(int, int)]:
        moves_list = list()
        empty_cells = self.cells - set(board)
        for move in empty_cells:
            if self.is_a_valid_action(board, move[0], move[1]):
                moves_list.append(move)
        return moves_list

    def check_winner(self, board: Board):
        empty_cells = self.cells - set(board)
        for move in empty_cells:
            if self.is_a_valid_action(board, move[0], move[1]):
                return False
        return True

    def simple_eval(self, board, player):
        # This evaluation function serves to prefer states in which the player has an even number of moves
        # This is because we reserve us another move after the opponent's move
        moves = self.actions(board)
        val = 1 - (len(moves) % 2)
        return val if player == 'R' else -val

