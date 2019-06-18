#
# Code by Abraham Montilla.
# Adapted from Carsten Friedrich (https://github.com/fcarsten/tic-tac-toe).
#

import numpy as np
from enum import Enum


class GameResult(Enum):
    """
    Enum to encode different states of the game. A game can be in progress (NOT_FINISHED), lost, won, or draw
    """
    NOT_FINISHED = 0
    YELLOW_WIN = 1
    RED_WIN = 2
    DRAW = 3


#
# Values to encode the current content of a field on the board. A field can be empty, contain a naught, or
# contain a cross
#
EMPTY = 0  # type: int
YELLOW = 1  # type: int
RED = 2  # type: int

#
# Define the length and width of the board. Has to be 3 at the moment, or some parts of the code will break. Also,
# the game mechanics kind of require this dimension unless other rules are changed as well. Encoding as a variable
# to make the code more readable
#
BOARD_W = 7  # type: int
BOARD_H = 6
BOARD_SIZE = BOARD_W * BOARD_H  # type: int


class Board:
    """
    The class to encode a Connect 4 board, including its current state of pieces.
    Also contains various utility methods.
    """

    def hash_value(self) -> int:
        """
        Encode the current state of the game (board positions) as an integer. Will be used for caching evaluations
        :return: A collision free hash value representing the current board state
        """
        res = 0
        for i in range(BOARD_SIZE):
            res *= 3
            res += int(self.state[i])

        return res

    @staticmethod
    def other_side(side: int) -> int:
        """
        Utility method to return the value of the other player than the one passed as input
        :param side: The side we want to know the opposite of
        :return: The opposite side to the one passed as input
        """
        if side == EMPTY:
            raise ValueError("EMPTY has no 'other side'")

        if side == RED:
            return YELLOW

        if side == YELLOW:
            return RED

        raise ValueError("{} is not a valid side".format(side))

    def __init__(self, s=None):
        """
        Create a new Board. If a state is passed in, we use that otherwise we initialize with an empty board
        :param s: Optional board state to initialise the board with
        """
        self.col_heights = np.array([0, 0, 0, 0, 0, 0, 0])

        if s is None:
            self.state = np.zeros(BOARD_SIZE)
            self.reset()
        else:
            self.state = s.copy()
            self.calc_col_heights()

    def calc_col_heights(self):
        b = self.state

        for c in range(BOARD_W):
            for r in range(BOARD_H):
                pos = self.coord_to_pos((r, c))
                if b[pos] != EMPTY:
                    self.col_heights[c] = BOARD_H - r
                    break

    def coord_to_pos(self, coord: (int, int)) -> int:
        """
        Converts a 2D board position to a 1D board position.
        Various parts of code prefer one over the other.
        :param coord: A board position in 2D coordinates
        :return: The same board position in 1D coordinates
        """
        return coord[0] * BOARD_W + coord[1]

    def pos_to_coord(self, pos: int) -> (int, int):
        """
        Converts a 1D board position to a 2D board position.
        Various parts of code prefer one over the other.
        :param pos: A board position in 1D coordinates
        :return: The same board position in 2D coordinates
        """
        return pos // BOARD_W, pos % BOARD_W

    def reset(self):
        """
        Resets the game board. All fields are set to be EMPTY.
        """
        self.state.fill(EMPTY)
        self.col_heights = np.array([0, 0, 0, 0, 0, 0, 0])

    def board_is_full(self) -> int:
        """
        Indicates if all the pieces in the board are being used.
        :return: Wether the board is full or not.
        """
        return sum(self.col_heights) == BOARD_SIZE

    def random_empty_spot(self) -> int:
        """
        Returns a random empty spot on the board in 1D coordinates
        :return: A random empty spot on the board in 1D coordinates
        """
        valid = False

        while not valid:
            col = np.random.randint(BOARD_W)
            h = self.col_heights[col]
            valid = h < BOARD_H

        row = BOARD_H - h - 1
        return self.coord_to_pos((row, col))

    def next_pos_in_col(self, col):
        """
        Returns the position where a chip could be placed, given a column in the board
        :param col: The column where the chip is meant to placed
        :return: The next free position (index) in the state array, based on the specified column
        """
        h = self.col_heights[col]
        row = BOARD_H - h - 1
        return self.coord_to_pos((row, col))

    def is_legal(self, pos: int) -> bool:
        """
        Tests whether a board position can be played, i.e. is currently empty
        :param pos: The board position in 1D that is to be checked
        :return: Whether the position can be played
        """
        row = pos // BOARD_W
        col = pos % BOARD_W

        height = self.col_heights[col]
        return (0 <= pos < BOARD_SIZE) and (height < BOARD_H) and (row == BOARD_H - height - 1)

    def valid_moves(self):
        """
        List of all the columns where a player could make a valid move
        :return: A list of column indexes (from 0 to 6) where a move can be made
        """
        # get column indices where there is still room to add chips.
        cols = (self.col_heights < BOARD_H).nonzero()[0]
        return [self.next_pos_in_col(i) for i in cols]

    def move(self, position: int, side: int) -> (np.ndarray, GameResult, bool):
        """
        Places a piece of side "side" at position "position". The position is to be provided as 1D.
        Throws a ValueError if the position is not EMPTY
        returns the new state of the board, the game result after this move, and whether this move has finished the game

        :param position: The position where we want to put a piece
        :param side: What piece we want to play (YELLOW, or RED)
        :return: The game state after the move, The game result after the move, Whether the move finished the game
        """

        if not self.is_legal(position):
            print('Illegal move')
            raise ValueError("Invalid move")

        self.state[position] = side
        self.col_heights[position % BOARD_W] += 1

        if self.check_win():
            return self.state, GameResult.RED_WIN if side == RED else GameResult.YELLOW_WIN, True

        if self.board_is_full():
            return self.state, GameResult.DRAW, True

        return self.state, GameResult.NOT_FINISHED, False

    def who_won(self) -> int:
        """
        Check whether either side has won the game and return the winner
        :return: If one player has won, that player; otherwise EMPTY
        """
        cell = lambda i, j: self.state[self.coord_to_pos((i, j))]

        for i in range(BOARD_H-1, -1, -1):
            for j in range(0, BOARD_W):
                player = cell(i, j)

                if player == EMPTY:
                    continue

                   # Checking for horizontal lines.
                if ((j + 3 < BOARD_W and player == cell(i, j+3) == cell(i, j+2) == cell(i, j+1)) or
                      # Check vertical lines only when the height of the column has 4 or more chips.
                      (self.col_heights[j] > 3 and i - 2 > 0 and player == cell(i-3, j) == cell(i-2, j) == cell(i-1, j)) or
                      # Checking for top-right diagonals.
                      (i - 2 > 0 and j + 3 < BOARD_W and player == cell(i-3, j+3) == cell(i-2, j+2) == cell(i-1, j+1)) or
                      # Checking for top-left diagonals.
                      (i - 2 > 0 and j - 2 > 0 and player == cell(i-3, j-3) == cell(i-2, j-2) == cell(i-1, j-1))):
                    return player

        return EMPTY

    def check_win(self) -> bool:
        """
        Check whether either side has won the game
        :return: Whether a side has won the game
        """
        return self.who_won() != EMPTY

    def state_to_char(self, pos, html=False):
        """
        Return 'x', 'o', or ' ' depending on what piece is on 1D position pos. Ig `html` is True,
        return '&ensp' instead of ' ' to enforce a white space in the case of HTML output
        :param pos: The position in 1D for which we want a character representation
        :param html: Flag indicating whether we want an ASCII (False) or HTML (True) character
        :return: 'x', 'o', or ' ' depending on what piece is on 1D position pos. Ig `html` is True,
        return '&ensp' instead of ' '
        """
        if (self.state[pos]) == EMPTY:
            return '&ensp;' if html else ' '

        if (self.state[pos]) == YELLOW:
            return 'o'

        return 'x'

    def html_str(self) -> str:
        """
        Format and return the game state as a HTML table
        :return: The game state as a HTML table string
        """
        data = self.state_to_charlist(True)
        html = '<table border="1"><tr>{}</tr></table>'.format(
            '</tr><tr>'.join(
                '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data)
        )
        return html

    def state_to_charlist(self, html=False):
        """
        Convert the game state to a list of list of strings (e.g. for creating a HTML table view of it).
        Useful for displaying the current state of the game.
        :param html: Flag indicating whether we want an ASCII (False) or HTML (True) character
        :return: A list of lists of character representing the game state.
        """
        res = []
        for i in range(3):
            line = [self.state_to_char(i * 3, html),
                    self.state_to_char(i * 3 + 1, html),
                    self.state_to_char(i * 3 + 2, html)]
            res.append(line)

        return res

    def val_to_disc(self, value):
        """
        Coloring for the chips printed on the terminal.
        :param value: Either RED, YELLOW or EMPTY.
        :return: Either a red disc, yellow disc or blank space depending on the given value
        """
        if value == EMPTY:
            return ' '
        elif value == YELLOW:
            return "\033[93m●\033[00m"
        else:
            return "\033[91m●\033[00m"

    def __str__(self) -> str:
        """
        Return ASCII representation of the board
        :return: ASCII representation of the board
        """
        lim = BOARD_W * (BOARD_H - 1)
        buf = '\n'

        for i, v in enumerate(self.state):
            v = self.val_to_disc(v)
            sep = '--+---+---+---+---+---+---' if i < lim else ''
            buf += '{}{}{}'.format(v, ' | ' if (i+1) % BOARD_W else '\n' + sep, '' if (i+1) % BOARD_W else '\n')

        return buf[:-1]

    def print_board(self):
        """
        Print an ASCII representation of the board
        """
        for i in range(3):
            board_str = self.state_to_char(i * 3) + '|' + self.state_to_char(i * 3 + 1) \
                        + '|' + self.state_to_char(i * 3 + 2)

            print(board_str)
            if i != 2:
                print("-----")

        print("")
