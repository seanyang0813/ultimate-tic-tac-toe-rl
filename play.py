from game import Game, Player
from random import randint


if __name__ == '__main__':
    game = Game()
    state = game.is_game_over_and_winner()
    depth = 100000
    state = (False, Player.EMPTY)
    tried = set()
    while state[0] == False and depth > 0:
        x = randint(0, 8)
        y = randint(0, 8)
        if (x, y) in tried:
            continue
        tried.add((x, y))
        if game.is_move_allowed(x, y):
            game.make_move(x, y)
            game.print_board()
            state = game.is_game_over_and_winner()
            if (state[0] == True):
                break
        else:
            print('invalid move', x, y)
        depth -= 1
    print(state)
    if (state != None):
        print('winner is', state[1])
    print("undoing moves ..................................................................................")
    while len(game.move_history) > 0:
        game.undo_move()
        game.print_board()
        state = game.is_game_over_and_winner()
        if (state[0] == True):
            print("shouldn't happen")
            break