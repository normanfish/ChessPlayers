import chess
from chess import Board


class StateMCST:
    def __init__(self, board: Board):
        self.board = board

    def getCurrentPlayer(self):
        return 1 if self.board.turn else -1

    def getPossibleActions(self):
        return list(self.board.legal_moves)

    def takeAction(self, action):
        timid = self.board.copy()
        timid.push(action)
        nextS = StateMCST(timid)
        return nextS

    def isTerminal(self):
        return self.board.is_game_over()

    def getReward(self):
        result = self.board.result()
        if result == '1-0':
            return 1
        if result == '0-1':
            return -1
        else:
            return 0
