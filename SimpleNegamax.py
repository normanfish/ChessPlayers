"""
Simplest implementation of an AI Player. Done using a simplified version of Claude Shannon's (1949) evaluation,
that only considers material difference. The Tree Search Algorithm employed is a plain Negamax algorithm with no
optimizations.
"""
import chess
import AIPlayer
import math
import random
import Eval1


class SimpleNegamax(AIPlayer.AIPlayer):

    def __init__(self, color):
        super().__init__(color)
        self.__depth = 3
        self.__to_return = chess.Move.null()

    def make_move(self, board: chess.Board):
        if board.fullmove_number == 1:
            possible_moves = list(board.legal_moves)
            self.__to_return = random.choice(possible_moves)
        else:
            self.__negamax_tree(board, 0, 1 if self.color == 'w' else -1)
        return self.__to_return

    def evaluate(self, board: chess.Board):
        if board.is_checkmate():
            return 9001  # insert "it's over 9000" Vegeta DBZ meme
        # basically the simplest weights I know
        queen_weights, bishop_weights, rook_weights, knight_weights, pawn_weights = 9, 3, 5, 3, 1
        return Eval1.AmateurEval.material_diff(board, queen_weights, bishop_weights, rook_weights,
                                               knight_weights, pawn_weights)

    def __negamax_tree(self, board, curr_depth, ev_sign):
        if curr_depth == self.__depth:
            leaf_score = self.evaluate(board)
            return leaf_score * ev_sign
        level_best = -math.inf
        score = 0
        for move in board.legal_moves:
            board.push(move)
            score = -1 * self.__negamax_tree(board, curr_depth + 1, -ev_sign)
            if score > level_best:
                if curr_depth == 0:
                    self.__to_return = move
                level_best = score
            board.pop()
        return score
