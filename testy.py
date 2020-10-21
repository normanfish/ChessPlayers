from StockFishEngine import StockFishEngine
from MCNode import Node
import chess
import copy
import random

if __name__ == '__main__':
    a = Node(chess.Move.null())
    b = Node(chess.Move.null(), parent=a)
    c = Node(chess.Move.null(), parent=a)
    d = Node(chess.Move.null(), parent=b)
    e = Node(chess.Move.null(), parent=c)
    print("id a:" + id(a).__str__())
    print("id b:" + id(b).__str__())
    print("id c:" + id(c).__str__())
    print("id d:" + id(d).__str__())
    print("id e:" + id(e).__str__())
    test = copy.copy(a)
    while not test.is_leaf:
        print("id test node:" + id(test).__str__())
        test = random.choice(test.children)
