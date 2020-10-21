"""
An amateur evaluation engine, loosely following the outline by https://www.chessprogramming.org/Evaluation
The evaluation considers:   Material Advantage - Weights taken from Stockfish
                            Piece Location - Taken from secondchess
                            Pawn Structure -
                            King Safety -
                            Mobility - taken from stockfish's middle game evaluation
                            Note: Basic Start and End Game Lookups are implemented in the player
"""

import AIPlayer
import chess
from multiprocessing import *


class AmateurEval:
    def __init__(self, col: bool):

        self.__color = col
        temp = 2
        self.__stockfish_pawn_weight = 198 / temp
        self.__stockfish_knight_weight = 817 / temp
        self.__stockfish_bishop_weight = 836 / temp
        self.__stockfish_rook_weight = 1276 / temp
        self.__stockfish_queen_weight = 2521 / temp
        self.secondchess_pawn_piece_table = [0, 0, 0, 0, 0, 0, 0, 0,
                                             25, 25, 25, 25, 25, 25, 25, 25,
                                             18, 18, 18, 18, 18, 18, 18, 18,
                                             15, 15, 15, 15, 15, 15, 15, 15,
                                             10, 10, 10, 10, 10, 10, 10, 10,
                                             5, 5, 5, 5, 5, 5, 5, 5,
                                             0, 0, 0, -25, -25, 0, 0, 0,
                                             0, 0, 0, 0, 0, 0, 0, 0]
        self.secondchess_knight_piece_table = [-40, -25, -25, -25, -25, -25, -25, -40,
                                               -30, 0, 0, 0, 0, 0, 0, -30,
                                               -30, 0, 0, 0, 0, 0, 0, -30,
                                               -30, 0, 25, 45, 45, 25, 0, -30,
                                               -30, 0, 25, 45, 45, 25, 0, -30,
                                               -30, 0, 10, 0, 0, 10, 0, -30,
                                               -30, 0, 0, 5, 5, 0, 0, -30,
                                               -40, -30, -25, -25, -25, -25, -30, -40]
        self.secondchess_bishop_piece_table = [-10, 0, 0, 0, 0, 0, 0, -10,
                                               -10, 5, 0, 0, 0, 0, 5, -10,
                                               -10, 0, 5, 0, 0, 5, 0, -10,
                                               -10, 0, 0, 10, 10, 0, 0, -10,
                                               -10, 0, 5, 10, 10, 5, 0, -10,
                                               -10, 0, 5, 0, 0, 5, 0, -10,
                                               -10, 5, 0, 0, 0, 0, 5, -10,
                                               -10, -20, -20, -20, -20, -20, -20, -10]
        self.secondchess_rook_piece_table = [0, 0, 0, 0, 0, 0, 0, 0,
                                             20, 20, 20, 20, 20, 20, 20, 20,
                                             10, 10, 10, 10, 10, 10, 10, 10,
                                             5, 5, 5, 5, 5, 5, 5, 5,
                                             0, 0, 0, 0, 0, 0, 0, 0,
                                             0, 0, 0, 0, 0, 0, 0, 0,
                                             0, 0, 0, 0, 0, 0, 0, 0,
                                             0, 0, 0, 50, 50, 0, 0, 0]
        self.secondchess_king_piece_table = [-25, -25, -25, -25, -25, -25, -25, -25,
                                             -25, -25, -25, -25, -25, -25, -25, -25,
                                             -25, -25, -25, -25, -25, -25, -25, -25,
                                             -25, -25, -25, -25, -25, -25, -25, -25,
                                             -25, -25, -25, -25, -25, -25, -25, -25,
                                             -25, -25, -25, -25, -25, -25, -25, -25,
                                             -25, -25, -25, -25, -25, -25, -25, -25,
                                             10, 15, -15, -15, -15, -15, 15, 10]
        self.secondchess_flip = [56, 57, 58, 59, 60, 61, 62, 63,
                                 48, 49, 50, 51, 52, 53, 54, 55,
                                 40, 41, 42, 43, 44, 45, 46, 47,
                                 32, 33, 34, 35, 36, 37, 38, 39,
                                 24, 25, 26, 27, 28, 29, 30, 31,
                                 16, 17, 18, 19, 20, 21, 22, 23,
                                 8, 9, 10, 11, 12, 13, 14, 15,
                                 0, 1, 2, 3, 4, 5, 6, 7]
        self.__piece_tables = {chess.PAWN: self.secondchess_pawn_piece_table,
                               chess.KNIGHT: self.secondchess_knight_piece_table,
                               chess.BISHOP: self.secondchess_bishop_piece_table,
                               chess.ROOK: self.secondchess_rook_piece_table,
                               chess.KING: self.secondchess_king_piece_table}
        self.stockfish_mobility_knight = [-75, -56, -9, -2, 6, 15, 22, 30, 36]
        self.stockfish_mobility_rook = [-56, -25, -11, -5, -4, -1, 8, 14, 21, 23, 31, 32, 43, 49, 59]
        self.stockfish_mobility_bishop = [-48, -21, 16, 26, 37, 51, 54, 63, 65, 71, 79, 81, 92, 97]
        self.stockfish_mobility_queen = [-40, -25, 2, 4, 14, 24, 25, 40, 43, 47, 54, 56, 60, 70, 72, 73, 75, 77, 85, 94,
                                         99, 108, 112, 113, 118, 119, 123, 128]
        self.mobility_tables = {chess.KNIGHT: self.stockfish_mobility_knight,
                                chess.ROOK: self.stockfish_mobility_rook,
                                chess.QUEEN: self.stockfish_mobility_queen,
                                chess.BISHOP: self.stockfish_mobility_bishop}

    @staticmethod
    def material_diff(board: chess.Board, queens_weights, bishops_weights, rooks_weights,
                      knights_weights, pawns_weights):
        score = 0
        board_string = board.__str__()
        white_symbols = ['Q', 'R', 'B', 'N', 'P']
        black_symbols = ['q', 'r', 'b', 'n', 'p']
        weights = [queens_weights, rooks_weights, bishops_weights, knights_weights, pawns_weights]
        for i in range(5):
            score += weights[i] * (AIPlayer.AIPlayer.num_of_piece(white_symbols[i], board_string) -
                                   AIPlayer.AIPlayer.num_of_piece(black_symbols[i], board_string))
        return score

    def piece_location_score(self, board: chess.Board):
        score = 0
        for piece in chess.PIECE_TYPES:
            if piece == chess.QUEEN:
                continue
            for square in board.pieces(piece, self.__color):
                index = square if not self.__color else self.secondchess_flip[square]
                score += self.__piece_tables[piece][index]
        return score

    @staticmethod
    def king_safety(board: chess.Board):
        pass

    def mobility(self, board: chess.Board):
        score, mobilit_count = 0, 0
        for piece in range(chess.KNIGHT, chess.KING):  # iterate over all pieces that have meaningful mobility
            for minor_piece_square in board.pieces(piece,
                                                   self.__color):  # go over the separate instances of each minor piece
                score += self.mobility_tables[piece][chess.Board.attacks(board, minor_piece_square).__len__()]
        return score

    def evaluate(self, board: chess.Board):
        if board.is_checkmate():
            if board.result() == '1-0':
                return 9001  # insert "it's over 9000" Vegeta DBZ meme
            else:
                return -9001
        sum = AmateurEval.material_diff(board, self.__stockfish_queen_weight, self.__stockfish_bishop_weight,
                                        self.__stockfish_rook_weight, self.__stockfish_knight_weight,
                                        self.__stockfish_pawn_weight)
        mult = 1 if self.__color else -1
        sum += self.piece_location_score(board) * mult
        sum += self.mobility(board) * mult
        return sum
