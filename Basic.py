import SimpleNegamaxalphabeta
import Eval1
import chess


class Basic(SimpleNegamaxalphabeta.Negamaxalphabeta):
    def __init__(self, color):
        super().__init__(color)
        self.__depth = 5
        self.__evaluator = Eval1.AmateurEval(color == 'w')

    def evaluate(self, board: chess.Board):
        eval_core = self.__evaluator.evaluate(board)
        return eval_core
