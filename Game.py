import AIPlayerFactory
import chess
import chess.svg
import _thread
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget
import time

COLOR_SELECT_MESSAGE = "Please select a color:\n\'b\' for black, \'w\' for white\n"
LEVEL_PROMPT_MESSAGE = "Input a level of AI player to play against\n"
MOVE_PROMPT = "Please make a move\n"
INVALID_MOVE_MESSAGE = "Invalid move\n"
WHITES_TURN_MESSAGE = "White's turn\n"
BLACKS_TURN_MESSAGE = "Black's turn\n"
WHITE_VICTORY_MESSAGE = "WHITE WINS!\n"
BLACK_VICTORY_MESSAGE = "BLACK WINS!\n"
PLAY_AGAIN_MESSAGE = "Play Again? (enter \"y\" for yes and any other key for no)\n"
DRAW_MESSAGE = "DRAW\n"
WHITE = 'w'
BLACK = 'b'
CHARACTERS = {"R": '\u265c', "N": '\u265e', "B": '\u265d', "Q": '\u265b', "K": '\u265a', "P": '\u265f',
              "r": '\u2656', "n": '\u2658', "b": '\u2657', "q": '\u2655', "k": '\u2654', "p": '\u2659', ".": '\uff3f',
              "\n": "\n", " ": ""}


class MainWindow(QWidget):
    def __init__(self):
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


def crappy_print(curr_board):
    new_board_iter = map(lambda x: CHARACTERS.get(x), curr_board.__str__())
    for i, letter in enumerate(new_board_iter):
        if i % 16 == 0:
            print((8 - int(i / 16)).__str__() + "  ", end='')
        print(" " + letter, end='')
    print("\n    a   b   c  d   e  f   g   h")


def print_victory_message(result):
    if result == '1-0':
        print(WHITE_VICTORY_MESSAGE)
    elif result == '0-1':
        print(BLACK_VICTORY_MESSAGE)
    else:
        print(DRAW_MESSAGE)


def parse_square(st):
    return (ord(st[0]) - ord('a')) + (int(st[1]) - 1) * 8


def run():
    play_again = True
    player_factory = AIPlayerFactory.AIPlayerFactory()
    while play_again:
        board.reset()
        is_testing = False
        user_color = input(COLOR_SELECT_MESSAGE)
        level = input(LEVEL_PROMPT_MESSAGE)
        user_is_white = user_color == WHITE
        ai_player = player_factory.get_player(level + ('w' if user_color == 'b' else 'b'))
        dumb_player = player_factory.get_player('0' + user_color)
        # crappy_print(board)
        while not board.is_game_over():
            print(WHITES_TURN_MESSAGE) if board.turn else print(BLACKS_TURN_MESSAGE)
            if board.turn == user_is_white:
                if not is_testing:
                    move = input(MOVE_PROMPT)
                    try:
                        board.push_uci(move)
                    except ValueError:
                        print(INVALID_MOVE_MESSAGE)
                else:
                    board.push(dumb_player.make_move(board))
                    print(board.peek())
            else:
                board.push(ai_player.make_move(board))
                print(board.peek())
            # crappy_print(board)
            # if is_testing:
            #     time.sleep(2)
        print_victory_message(board.result())
        user_input_play_again = input(PLAY_AGAIN_MESSAGE)
        play_again = user_input_play_again == "y"


if __name__ == "__main__":
    board = chess.Board()
    _thread.start_new_thread(run, ())
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
