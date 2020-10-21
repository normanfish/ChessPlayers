import threading
import multiprocessing
import random
import chess
import time
import sys
from MCNode import Node
import os


class MCProcess(multiprocessing.Process):

    def __init__(self, board: Node, queue: multiprocessing.Queue, timeout):
        super(MCProcess, self).__init__(daemon=False)
        self.root = board
        self.queue = queue
        self.timeout = timeout

    def run(self):
        print("welcome to process: " + os.getpid().__str__())
        count = 1
        start_time, lap_start, lap_end = time.clock(), time.clock(), time.clock()
        while count < self.timeout * 5 + 1:
            leaf = self.select()
            assert (leaf in self.root.descendants)  # node should now be in the tree
            result = self.explore(leaf)
            self.propagate(leaf, result)
            if count % 50 == 0:
                lap_end = time.clock()
                print("process number: " + os.getpid().__str__() + " ran through " + (
                    count).__str__() + " games in: " + (
                              lap_end - start_time).__str__() + " seconds, the past 100 games took " + (
                              lap_end - lap_start).__str__() + " seconds")
                lap_start = time.clock()
            count += 1
        self.queue.put(self.root)
        sys.exit()

    def select(self):
        selected = self.root
        # as long as we don't have any unexplored children, we can go down the tree. We'll select the best node for
        # exploration using the UCI method from the current node's children
        while not selected.has_unexplored_children():
            # print("all children were tested")
            selected = max(selected.children, key=lambda x: x.UCI_formula())
        # we either have an unexplored child, or we have reached a terminal state. we'll check which case we are in
        if selected.is_terminal():
            # print("terminal state")
            # terminal state
            return selected
        # we have an unexplored child. we'll add it to the tree (expand phase) and return it
        # print("has unexplored child")
        unexplored_child = random.choice(selected.get_unexplored_children())
        expanded_new_node = Node(unexplored_child, parent=selected)
        return expanded_new_node

    def explore(self, leaf: Node):
        rollout_board = leaf.board.copy()
        while not rollout_board.is_game_over():
            move = random.choice(list(rollout_board.legal_moves))
            assert (isinstance(move, chess.Move))
            rollout_board.push(move)
        result = rollout_board.result().split(sep='-')[0]
        return result

    def propagate(self, leaf: Node, result):
        white_is_winner = result == '1'
        if result == '1/2':
            reward = 0.5
        elif leaf.board.turn != white_is_winner:
            reward = 0
        else:
            reward = 1
        while leaf != self.root:
            leaf.played_out += 1
            leaf.won += reward
            reward = 1 - reward
            leaf = leaf.parent
        self.root.played_out += 1
