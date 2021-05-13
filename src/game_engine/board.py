"""Board module containing board class and it's exceptions, handles the gameboard logic"""
from numpy import array
from .engine import BaseEngineStatus


class Board:
    """Handles the game board"""

    def __init__(self):
        self._players = ("x", "o", " ")
        self._board = array([[self._players[2]] * 3] * 3, dtype=str)
        self._next_play_by = "x"
        self._amount_of_moves_made = 0

    def add(self, location, item):
        """Adds and item to the location\n
        location should be an array with two numbers in it (numbers from 0 to 2)
        """
        if item != self._next_play_by:
            # if for some reason wrong player tries to move raise exception
            raise WrongPlayerException()
        if len(location) < 2:
            raise NotEnoughArgumentsException()
        if not (
            location[0] >= 0
            and location[0] <= 2
            and location[1] >= 0
            and location[1] <= 2
        ):
            raise OutsideBoardException()  # if outside the playing field raise exception

        if self._board[location] != " ":
            # if item at location is diffrent from 0 location is busy so we raise exception
            raise PositionTakenException()
        self._board[location] = item
        self._amount_of_moves_made += 1
        if self.run_checks(item):
            raise PlayerWonStatus(item)
        self._next_play_by = self._players[self._amount_of_moves_made % 2]

    def run_checks(self, item):
        """Runs all defined checks and returns True if any of them did"""
        return self._check_rows_for(item) or (
            self._check_columns_for(item) or self._check_diagonal_for(item)
        )

    def _check_rows_for(self, item):
        """Checks if any row is filled with an item\n
        returns True if there exists one, False otherwise"""
        return any((self._board == item).all(1))

    def _check_columns_for(self, item):
        """Checks if any column is filled with an item\n
        returns True if there exists one, False otherwise"""
        return any((self._board.T == item).all(1))

    def _check_diagonal_for(self, item):
        """Checks if any diagonal is filled with an item\n
        returns True if there exists one, False otherwise"""
        return all(self._board.diagonal() == item) or all(
            self._board[:, ::-1].diagonal() == item
        )


class BoardException(Exception):
    """Base for board class exceptions"""


class PlayerWonStatus(BaseEngineStatus):
    """Signals that a player won"""

    def __init__(self, player):
        BaseEngineStatus.__init__(self)
        self.player = player

    def __str__(self):
        return self.player + " has won the game"


class OutsideBoardException(BoardException):
    """Raised if the location is outside the board"""


class WrongPlayerException(BoardException):
    """Raised if the move is made by a wrong player"""


class PositionTakenException(BoardException):
    """Raised if the position is already taken by another item"""


class NotEnoughArgumentsException(BoardException):
    """Raised if the array doesn't have enough arguments to attempt to move"""
