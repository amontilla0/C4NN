#
# Copyright 2018 Carsten Friedrich (Carsten.Friedrich@gmail.com). All rights reserved
#

from c4nn.Board import Board, GameResult
from c4nn.Player import Player


class HumanPlayer(Player):
    """
    This player can play a game of Connect 4 by requesting inputs from a human.
    """

    def __init__(self):
        """
        Getting ready for playing Connect 4.
        """
        self.side = None
        super().__init__()

    def move(self, board: Board) -> (GameResult, bool):
        """
        Making a move taken from input
        :param board: The board to make a move on
        :return: The result of the move
        """
        valid = False
        while not valid
            try:
                print('please select a column[0-6]: ', end='')
                col = int(input())

                pos = board.next_pos_in_col(col)
                valid = board.is_legal(pos)
            except ValueError:
                print('not a valid number, try again.')

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
