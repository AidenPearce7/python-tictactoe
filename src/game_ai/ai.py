"""Module containing simple game AI"""
from random import randint
from ..game_engine.engine import Coordinates


class AI:
    """A simple bot"""

    def __init__(self, symbol="o"):
        self.free_coordinates = list(range(0, 9))
        self.symbol = symbol

    def make_random_move(self):
        """Make random list with random x,y coordinate"""
        random_field = randint(0, len(self.free_coordinates) - 1)
        return Coordinates(random_field % 3, random_field // 3, self.symbol)

    def add_move(self, coords):
        """Updates availble moves"""
        self.free_coordinates.remove(len(coords))
