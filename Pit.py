import AIPlayerFactory
import chess
import chess.svg
import _thread
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget

WHITE_LEVEL_PROMPT_MESSAGE = "Input a level for the white AI\n"
BLACK_LEVEL_PROMPT_MESSAGE = "Input a level for the black AI\n"
WHITES_TURN_MESSAGE = "White's turn\n"
BLACKS_TURN_MESSAGE = "Black's turn\n"
WHITE_VICTORY_MESSAGE = "WHITE WINS!\n"
BLACK_VICTORY_MESSAGE = "BLACK WINS!\n"
PLAY_AGAIN_MESSAGE = "Play Again? (enter \"y\" for yes and any other key for no)\n"
DRAW_MESSAGE = "DRAW\n"
WHITE = 'w'
BLACK = 'b'


class MainWindow(QWidget):
    def __init__(self,board):
        super().__init__()

        self.setGeometry(100, 100, 1080, 1920)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 1010, 990)

        self.chessboard = board

        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

    def paintEvent(self, event):
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)


def print_victory_message(result):
    if result == '1-0':
        print(WHITE_VICTORY_MESSAGE)
    elif result == '0-1':
        print(BLACK_VICTORY_MESSAGE)
    else:
        print(DRAW_MESSAGE)


def run():
    play_again = True
    player_factory = AIPlayerFactory.AIPlayerFactory()
    while play_again:
        board.reset()
        white_level = input(WHITE_LEVEL_PROMPT_MESSAGE)
        black_level = input(BLACK_LEVEL_PROMPT_MESSAGE)
        white_player = player_factory.get_player(white_level + 'w')
        black_player = player_factory.get_player(black_level + 'b')
        while not board.is_game_over():
            cop=board.copy()
            if board.turn:
                print(WHITES_TURN_MESSAGE)
                board.push(white_player.make_move(cop))
            else:
                print(BLACKS_TURN_MESSAGE)
                board.push(black_player.make_move(cop))
            print(board.peek())
        print_victory_message(board.result())
        user_input_play_again = input(PLAY_AGAIN_MESSAGE)
        play_again = user_input_play_again == "y"


if __name__ == "__main__":
    board = chess.Board()
    _thread.start_new_thread(run, ())
    app = QApplication([])
    window = MainWindow(board)
    window.show()
    app.exec()
