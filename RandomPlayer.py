from Player import Player
from random import randint

class RandomPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def play(self, b):
        played = False
        while not played:
            col = randint(0, 6)
            played = b.play(self.color, col)
