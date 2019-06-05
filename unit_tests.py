from Board import Board, Chip
from RandomPlayer import RandomPlayer
import numpy as np

b = Board()
#b = Board(np.array([0,0,0,0,0,0,0,   1,1,1,1,0,0,0,   0,0,0,0,0,0,0,   1,2,0,0,0,2,0,   1,0,2,0,2,0,0,   1,0,0,2,2,2,0   ]))
#b = Board(np.array([0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   1,1,1,0,0,0,0  ]))
#b = Board(np.array([2,0,2,1,1,2,0,   2,1,2,2,2,1,2,   1,2,1,1,2,2,1,   2,1,2,2,2,1,2,   2,2,2,1,1,1,2,   2,1,2,2,2,1,2   ]))

rp = RandomPlayer(Chip.RED)
yp = RandomPlayer(Chip.YELLOW)
plays = 0
players = [rp, yp]

b.play(Chip.YELLOW, 0)
b.play(Chip.RED, 0)
b.play(Chip.YELLOW, 6)
b.play(Chip.YELLOW, 6)
b.print_board()
print(b.state)
print()
#print(b.inputs)
print(b.inputs[0: 42])
print(b.inputs[42: 84])
print(b.inputs[84:])
# winner = False
#
# while not winner:
#     print('here...', b.col_heights)
#     players[plays % 2].play(b)
#     plays += 1
#     winner = b.check_for_winner()
#
# b.print_board()
#
# print('winner: {}, plays: {}'.format(winner, plays))
