import chess
import AIPlayer
import math
import random
import mcts
from StateForMCST import StateMCST


class MonteCarloEasy(AIPlayer.AIPlayer):
    def __init__(self, color):
        super().__init__(color)
        self.timelimit = 10000

    def make_move(self, board: chess.Board):
        mctree = mcts.mcts(self.timelimit)
        root = StateMCST(board)
        move = mctree.search(root)
        return move
