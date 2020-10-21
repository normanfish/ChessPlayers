import chess
import chess.engine
import AIPlayer


class StockFishEngine(AIPlayer.AIPlayer):
    def __init__(self, color):
        super().__init__(color)
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish_12.exe")
        print("stockfish loaded successfully")

    def make_move(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=1))
        return result.move
