import tensorflow as tf

from util import play_game
from c4nn.Board import Board
from c4nn.TFSessionManager import TFSessionManager
from c4nn.HumanPlayer import HumanPlayer
from c4nn.SimpleNNQPlayer import NNQPlayer
from c4nn.RndMinMaxAgent import RndMinMaxAgent
from c4nn.DeepExpDoubleDuelQPlayer import DeepExpDoubleDuelQPlayer
from numpy import array

board = Board()

nnplayer = DeepExpDoubleDuelQPlayer("DEDDPlayer1", win_value=10.0, loss_value=-10.0, learning_rate=0.001, training=False)
hmnplayer = HumanPlayer()
TFSessionManager.set_session(tf.Session())
TFSessionManager.load_session('models/models_session2')

sess = TFSessionManager.get_session()

print(play_game(board, nnplayer, hmnplayer, print_steps = True, reset_board=False, shift=False))

TFSessionManager.set_session(None)
