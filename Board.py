import numpy as np
from enum import IntEnum

class Chip(IntEnum):
    EMPTY = 0
    RED = 1
    YELLOW = 2
    DRAW = 3

BOARD_W = 7
BOARD_H = 6
BOARD_SIZE = BOARD_W * BOARD_H


class Board:
    def __init__(self, s=None):
        self.reset(s)

    def reset(self, s=None):
        self.col_heights = [0, 0, 0, 0, 0, 0, 0]
        if s is None:
            self.state = np.full((1, BOARD_SIZE), Chip.EMPTY, dtype=int)[0]
            self.inputs = np.concatenate((np.full((1, BOARD_SIZE * 2), 0, dtype=int)[0], np.full((1, BOARD_SIZE), 1, dtype=int)[0]))
        else:
            self.state = s.copy()
            self.board_to_inputs()
            self.calc_col_heights()

    def board_to_inputs(self):
        reds = np.full((1, BOARD_SIZE), 0, dtype=int)[0]
        yellows = np.full((1, BOARD_SIZE), 0, dtype=int)[0]
        empties = np.full((1, BOARD_SIZE), 0, dtype=int)[0]

        for idx, chip in enumerate(self.state):
            if chip == Chip.RED:
                reds[idx] = 1
            elif chip == Chip.YELLOW:
                yellows[idx] = 1
            else:
                empties[idx] = 1

        self.inputs = np.concatenate((reds, yellows, empties))

    def calc_col_heights(self):
        for c in range(0, BOARD_W):
            for r in range(0, BOARD_H):
                if self.get_cell(r, c) != Chip.EMPTY:
                    self.col_heights[c] = BOARD_H - r
                    break

    def print_board(self):
        print()
        lim = BOARD_W * (BOARD_H - 1)

        for i, v in enumerate(self.state):
            sep = '--+---+---+---+---+---+---' if i < lim else ''
            print('{}{}'.format(v, ' | ' if (i+1) % BOARD_W else '\n' + sep), end= '' if (i+1) % BOARD_W else '\n')

        print()

    def get_pos(self, i, j):
        return i * BOARD_W + j

    def get_cell(self, i, j):
        pos = self.get_pos(i, j)
        return self.state[pos]

    def check_for_winner(self):
        cell = self.get_cell

        for i in range(BOARD_H-1, -1, -1):
            for j in range(0, BOARD_W):
                player = cell(i, j)

                if player == Chip.EMPTY:
                    continue

                # Checking for horizontal lines.
                if j + 3 < BOARD_W and player == cell(i, j+3) == cell(i, j+2) == cell(i, j+1):
                    return (player, True)

                # Check vertical lines only when the height of the column has 4 or more chips.
                if self.col_heights[j] > 3 and i - 2 > 0 and player == cell(i-3, j) == cell(i-2, j) == cell(i-1, j):
                    return (player, True)

                # Checking for top-right diagonals.
                if i - 2 > 0 and j + 3 < BOARD_W and player == cell(i-3, j+3) == cell(i-2, j+2) == cell(i-1, j+1):
                    return (player, True)

                # Checking for top-left diagonals.
                if i - 2 > 0 and j - 2 > 0 and player == cell(i-3, j-3) == cell(i-2, j-2) == cell(i-1, j-1):
                    return (player, True)

        if sum(self.col_heights) == BOARD_H * BOARD_W:
            return (Chip.DRAW, True)

        return (Chip.EMPTY, False)

    def is_valid_move(self, col):
        height = self.col_heights[col]
        return (height, height < 6)

    def play(self, player, col):
        h, valid_move = self.is_valid_move(col)
        if valid_move:
            pos = self.get_pos(BOARD_H - h - 1, col)
            self.state[pos] = player
            self.inputs[(player-1) * BOARD_SIZE + pos] = 1
            self.inputs[BOARD_SIZE * 2 + pos] = 0
            self.col_heights[col] += 1
            return True

        return False

    def opponent(self, color):
        return Chip.RED if color == Chip.YELLOW else Chip.YELLOW
