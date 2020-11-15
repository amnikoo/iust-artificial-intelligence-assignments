import random
from time import sleep

class RandomAI():
    def __init__(self):
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)
        move = random.choice(moves)
        sleep(1)
        print("Random AI recommending move " + str(move))
        return move
