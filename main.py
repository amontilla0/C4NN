from Board import Board, Chip
from RandomPlayer import RandomPlayer
import numpy as np

b = Board()
rp = RandomPlayer(Chip.RED)
yp = RandomPlayer(Chip.YELLOW)
plays = 0
players = [rp, yp]

b.print_board()

winner = 0
done = False

while not done:
    players[plays % 2].play(b)
    plays += 1
    winner, done = b.check_for_winner()

b.print_board()

print('winner: {}, plays: {}'.format(winner, plays))
