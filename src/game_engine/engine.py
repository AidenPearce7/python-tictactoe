"""Engine module containing all classes and functions, handles the game"""

from .board import Board, DrawStatus, PlayerWonStatus


class Coordinates:
    """Represents a set of coordiantes"""

    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def get_coordinates(self):
        """returns a set of coordinates formated for the board"""
        return (self.y, self.x)

    def __len__(self):
        return self.y * 3 + self.x


class Engine:
    """Instance of the engine handling the game"""

    def __init__(self, starting_symbol):
        self.board = Board(starting_symbol)
        self.has_won = False
        self.winner = None

    def make_move(self, coords):
        """Tries to make a move"""
        if self.has_won:
            pass
        try:
            self.board.add(coords.get_coordinates(), coords.symbol)
        except PlayerWonStatus as won:
            self.has_won = True
            self.winner = won.player
        except DrawStatus:
            self.has_won = True
            self.winner = "DRAW"
        # all other exceptions should be delt with higher up

    def get_board_copy(self):
        """Returns copy of the game board for display"""
        return self.board.get_copy()

    def restart(self):
        """Restarts the game\n
        To be used for a new game or in case of errors"""
        self.board.clear()
        self.has_won = False
        self.winner = None
