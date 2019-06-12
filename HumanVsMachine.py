import tensorflow as tf

from util import play_game
from c4nn.Board import Board
from c4nn.TFSessionManager import TFSessionManager
from c4nn.HumanPlayer import HumanPlayer
from c4nn.SimpleNNQPlayer import NNQPlayer

board = Board()
nnplayer = NNQPlayer("QLearner", learning_rate=0.01, win_value=100.0, loss_value=-100.0, training=False)
hmnplayer = HumanPlayer()

TFSessionManager.set_session(tf.Session())
TFSessionManager.load_session('models/SimpleNNQPlayer')

sess = TFSessionManager.get_session()

print(play_game(board, nnplayer, hmnplayer, print_steps = True))

TFSessionManager.set_session(None)
