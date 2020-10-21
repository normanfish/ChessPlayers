import chess
import AIPlayer
import copy
import numpy
from MCNode import Node
from MCProcess import MCProcess
from time import sleep
from multiprocessing import cpu_count, Queue


class MonteCarlo(AIPlayer.AIPlayer):
    def __init__(self, color):
        super().__init__(color)
        self.num_threats = cpu_count() - 1
        self.root = Node(chess.Board.empty())

    def make_move(self, board: chess.Board):
        # init threads, run and join them, and combine their trees
        self.root = Node(board.copy())
        workers = []
        roots_queue = Queue(self.num_threats)
        scores = {}
        for _ in range(self.num_threats):
            new_root = Node(copy.deepcopy(board))
            t1 = MCProcess(new_root, roots_queue, 60)
            workers.append(t1)
            t1.start()
        sleep(65)

        total = 0
        while not roots_queue.empty():
            root = roots_queue.get()
            for child in root.children:
                move = child.board.pop().__str__()
                if move not in scores.keys():
                    scores[move] = (child.won, child.played_out)
                else:
                    prev_win = scores[move][0]
                    prev_played_out = scores[move][1]
                    scores[move] = (child.won + prev_win, child.played_out + prev_played_out)
                total += child.played_out
            print(total)
        best_move = min(scores, key=scores.get)
        print("best move is " + best_move.__str__())
        return chess.Move.from_uci(best_move)
