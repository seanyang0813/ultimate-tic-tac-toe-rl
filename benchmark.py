from game import Game, Player
from agent_play import RandomAgent
from tianshou_play import RLAgent
import random

game = Game()
random_agent = RandomAgent()
rl_agent = RLAgent()
# track score from RL agent perspective
score = {"win": 0, "loss": 0, "draw": 0}
for i in range(1000):
    # choose a random person to start first 
    start = None
    game = Game()
    rl_playing = None
    if random.random() > 0.5:
        start = random_agent
        rl_playing = Player.O
    else:
        start = rl_agent
        rl_playing = Player.X
    print('rl playing', rl_playing)
    # play the game
    while game.is_game_over_and_winner()[0] == False:
        if start == random_agent:
            random_agent.play_move(game)
            if (game.is_game_over_and_winner()[0] == False):
                rl_agent.play_move(game)
        else:
            rl_agent.play_move(game)
            if (game.is_game_over_and_winner()[0] == False):
                random_agent.play_move(game)
            
    winner = game.is_game_over_and_winner()[1]
    print("winner is", winner)
    if (winner == rl_playing):
        score["win"] += 1
    elif (winner == Player.EMPTY):
        score["draw"] += 1
    else:
        score["loss"] += 1

print(score)
