import tensorflow as tf
import matplotlib.pyplot as plt

from util import evaluate_players
from c4nn.TFSessionManager import TFSessionManager
from c4nn.RandomPlayer import RandomPlayer
from c4nn.SimpleNNQPlayer import NNQPlayer

train = True

nnplayer = NNQPlayer("QLearner", learning_rate=0.01, win_value=100.0, loss_value=-100.0, training=train)
rndplayer = RandomPlayer()

TFSessionManager.set_session(tf.Session())

if not train:
    TFSessionManager.load_session('models/SimpleNNQPlayer')

sess = TFSessionManager.get_session()

if train:
    sess.run(tf.global_variables_initializer())

# num battles
nb = 200
# games per battle
gpb = 100

game_number, p1_wins, p2_wins, draws = evaluate_players(nnplayer, rndplayer, num_battles = nb, games_per_battle=gpb)

if train:
    TFSessionManager.save_session('models/SimpleNNQPlayer')

plt.plot(game_number, draws, color=(0.7, 0.7, 0.7), label='draws')
plt.plot(game_number, p1_wins, 'r-', label='player 1')
plt.plot(game_number, p2_wins, 'y-', label='player 2')
plt.xlabel('battle iterations ({} games per battle)'.format(gpb))
plt.ylabel('battle winning ratio (%)')
plt.legend(loc='best')

plt.show()
TFSessionManager.set_session(None)
