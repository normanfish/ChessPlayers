"""
A slightly more complex negamax player with claude's evaluation technique, that uses alpha beta pruning to improve
performance
"""
import chess
import SimpleNegamax
import math


class Negamaxalphabeta(SimpleNegamax.SimpleNegamax):

    def __init__(self, color):
        super().__init__(color)
        self.__depth = 5

    def make_move(self, board: chess.Board):
        score = self.__negamax_alpha_beta(board, 0,  -math.inf, math.inf)
        print("best score was: " + score.__str__())
        return self.__to_return

    def __negamax_alpha_beta(self, board, curr_depth, alpha, beta):
        if curr_depth == self.__depth:
            leaf_score = self.evaluate(board)
            return leaf_score
        level_best = -math.inf
        score = 0
        for move in board.legal_moves:
            board.push(move)
            score = -self.__negamax_alpha_beta(board, curr_depth + 1, -beta, -alpha)
            board.pop()
            if score > level_best:
                if curr_depth == 0:
                    self.__to_return = move
                level_best = score
                alpha = max(alpha, level_best)
            if alpha >= beta:
                break
        return score
