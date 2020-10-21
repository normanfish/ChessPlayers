"""
Chooses randomly from all possible moves
"""
import AIPlayer
import chess
import random


class RandomPlayer(AIPlayer.AIPlayer):
    def make_move(self, board: chess.Board):
        possible_moves = list(board.legal_moves)
        return random.choice(possible_moves)
