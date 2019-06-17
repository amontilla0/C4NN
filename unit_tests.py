import numpy as np
import matplotlib.pyplot as plt
from c4nn.Board import Board
from c4nn.RandomPlayer import RandomPlayer
from util import play_game, evaluate_players

b = Board()
#b = Board(np.array([0,0,0,0,0,0,0,   1,1,1,1,0,0,0,   0,0,0,0,0,0,0,   1,2,0,0,0,2,0,   1,0,2,0,2,0,0,   1,0,0,2,2,2,0   ]))
#b = Board(np.array([0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   1,1,1,0,0,0,0  ]))
# close to draw
#b = Board(np.array([2,0,2,1,1,2,0,   2,1,2,2,2,1,2,   1,2,1,1,2,2,1,   2,1,2,2,2,1,2,   2,2,2,1,1,1,2,   2,1,2,2,2,1,2   ]))
# draw
#b = Board(np.array([2,1,2,1,1,2,1,   2,1,2,2,2,1,2,   1,2,1,1,2,2,1,   2,1,2,2,2,1,2,   2,2,2,1,1,1,2,   2,1,2,2,2,1,2   ]))
y = []

def empty_sampling():
    for i in range(1000):
        c = b.random_empty_spot()
        y.append(c)

    #print(y)
    print(sum(y) / len(y))

def wins():
    print(b.who_won())

def play_one():
    p1 = RandomPlayer()
    p2 = RandomPlayer()

    res = play_game(b, p1, p2, True)

    print (res)
    #print(b)

def play_n_plot():
    r1 = RandomPlayer()
    r2 = RandomPlayer()
    game_number, p1_wins, p2_wins, draws = evaluate_players(r1, r2, num_battles=100)

    p = plt.plot(game_number, draws, 'r-', game_number, p1_wins, 'g-', game_number, p2_wins, 'b-')

    plt.show()

def hash_checks():
    b1 = Board(
    np.array([1,0,0,0,0,0,0,
              2,0,0,0,0,0,0,
              1,0,0,0,0,0,0,
              2,0,0,0,0,0,0,
              2,0,0,0,0,0,0,
              2,2,0,1,1,1,0   ])
    )

    b2 = Board(
    np.array([1,0,0,0,0,0,0,
              2,0,0,0,0,0,0,
              1,0,0,0,0,0,0,
              2,0,0,0,0,0,0,
              2,0,0,0,0,0,0,
              2,0,0,1,1,0,0   ])
    )

    b3 = Board(
    np.array([2,2,2,2,2,2,2,
              2,2,2,2,2,2,2,
              2,2,2,2,2,2,2,
              2,2,2,2,2,2,2,
              2,2,2,2,2,2,2,
              2,2,2,2,2,2,1   ])
    )

    b4 = Board(
    np.array([2,2,2,2,2,2,2,
              2,2,2,2,2,2,2,
              2,2,2,2,2,2,2,
              2,2,2,2,2,2,2,
              2,2,2,2,2,2,2,
              2,2,2,2,2,2,2   ])
    )

    print(b1, b2)
    print(int(b1.hash_value()))
    print(int(b2.hash_value()))

    print(b1.hash_value() == b2.hash_value())

    print(int(b3.hash_value()))
    print(int(b4.hash_value()))

    print(b3.hash_value() == b4.hash_value())

    # import pdb; pdb.set_trace()

    return b1, b2


#empty_sampling()

#play_n_plot()

a, b = hash_checks()
