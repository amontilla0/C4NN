#
# Copyright 2018 Carsten Friedrich (Carsten.Friedrich@gmail.com). All rights reserved
#

from c4nn.Board import Board, GameResult
from c4nn.Player import Player


class RandomPlayer(Player):
    """
    This player can play a game of Tic Tac Toe by randomly choosing a free spot on the board.
    It does not learn or get better.
    """

    def __init__(self):
        """
        Getting ready for playing tic tac toe.
        """
        self.side = None
        super().__init__()

    def move(self, board: Board) -> (GameResult, bool):
        """
        Making a random move
        :param board: The board to make a move on
        :return: The result of the move
        """
        pos = board.random_empty_spot()
        _, res, finished = board.move(pos, self.side)
        return res, finished

    def final_result(self, result: GameResult):
        """
        Does nothing.
        :param result: The result of the game that just finished
        :return:
        """
        pass

    def new_game(self, side: int):
        """
        Setting the side for the game to come. Noting else to do.
        :param side: The side this player will be playing
        """
        self.side = side
