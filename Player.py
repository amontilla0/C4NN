from abc import ABC, abstractmethod
from Board import Board

class Player(ABC):
    def __init__(self, c):
        super().__init__()
        self.color = c

    @abstractmethod
    def play(b):
        pass
