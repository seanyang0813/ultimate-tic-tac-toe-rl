# take in game look at the board and make a move

from game import Game, Player
import random

class RandomAgent:
    # assume you are next to move
    def play_move(self, game: Game):
        # get the board
        valid_moves = game.get_all_valid_moves()
        if len(valid_moves) == 0:
            return None
        else:
            move = random.choice(valid_moves)
            game.make_move(move[0], move[1])
            return move