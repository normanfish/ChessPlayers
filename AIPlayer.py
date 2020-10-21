import chess

"""the general class for an AI opponent"""


class AIPlayer():
    def __init__(self, color):
        self.color = color

    def make_move(self, board):
        pass

    @staticmethod
    def num_of_piece(piece, string):
        return string.count(piece)
