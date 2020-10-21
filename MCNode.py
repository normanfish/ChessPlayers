from anytree import NodeMixin
from chess import Board
import math


class Node(NodeMixin):
    def __init__(self, board: Board, parent=None, children=None):
        self.board = board
        self.won = 0
        self.played_out = 0
        if children:
            self.children = children
        self.parent = parent
        self.possible_moves = list(self.board.legal_moves)

    def has_unexplored_children(self):
        num_visited_children = len(self.children)
        num_possible_moves = len(self.possible_moves)
        #print("explored: " + num_visited_children.__str__() + " vs possible:" + num_possible_moves.__str__())
        return num_possible_moves != num_visited_children

    def get_unexplored_children(self):
        explored_boards = list(child.board for child in self.children)
        possible_children = list()
        for move in self.possible_moves:
            temp = self.board.copy()
            temp.push(move)
            possible_children.append(temp)
        unexplored_boards = [x for x in possible_children if x not in explored_boards]
        assert (unexplored_boards.__len__() == len(self.possible_moves) - len(self.children))
        return unexplored_boards

    def is_terminal(self):
        return self.board.is_checkmate()

    def UCI_formula(self):
        avg_reward = self.won / self.played_out
        assert isinstance(self.parent, Node)
        times_parents_tried = self.parent.played_out
        final = avg_reward + math.sqrt(2 * times_parents_tried / self.played_out)
        return final
