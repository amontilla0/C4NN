import tensorflow as tf
import matplotlib.pyplot as plt

from util import evaluate_players
from c4nn.TFSessionManager import TFSessionManager
from c4nn.RandomPlayer import RandomPlayer
# from c4nn.SimpleNNQPlayer import NNQPlayer
from c4nn.RndMinMaxAgent import RndMinMaxAgent
# from c4nn.DirectPolicyAgent import DirectPolicyAgent
from c4nn.DeepExpDoubleDuelQPlayer import DeepExpDoubleDuelQPlayer

train = False

dddplayer = DeepExpDoubleDuelQPlayer("DEDDPlayer1", win_value=10.0, loss_value=-10.0, learning_rate=0.001)

rndplayer = RandomPlayer()
rmmplayer = RndMinMaxAgent(3)

TFSessionManager.set_session(tf.Session())

if not train:
    TFSessionManager.load_session('models/SimpleNNQPlayer')

sess = TFSessionManager.get_session()

if train:
    sess.run(tf.global_variables_initializer())

# num battles
nb = 500
# games per battle
gpb = 100

game_number, p1_wins, p2_wins, draws = evaluate_players(dddplayer, rmmplayer, num_battles = nb, games_per_battle=gpb)

if train:
    TFSessionManager.save_session('models/models_session2')

plt.plot(game_number, draws, color=(0.7, 0.7, 0.7), label='draws')
plt.plot(game_number, p1_wins, 'r-', label='player 1')
plt.plot(game_number, p2_wins, 'y-', label='player 2')
plt.xlabel('battle iterations ({} games per battle)'.format(gpb))
plt.ylabel('battle winning ratio (%)')
plt.legend(loc='best')

plt.show()
TFSessionManager.set_session(None)
