# Description
Let me preface this with this is a really weak bot
The win, draw, loss rate are 86%, 8%, and 5% and I can even easily beat it as a human

![Screenshot from 2024-03-10 22-44-49](https://github.com/Algorithm-Arena/weekly-challenge-8-ultimate-tic-tac-toe/assets/32753704/c18a021a-b52c-47e9-a543-3ee019ea51e8)

The multi agent training environment is modified from https://pettingzoo.farama.org/environments/classic/tictactoe/ 
Training code is modified from https://github.com/thu-ml/tianshou/blob/master/test/pettingzoo/tic_tac_toe.py
I implemented the rules of ultimate tic tac toe and UI myself.
It uses reinforment learning algorithm to take in board state and output the action based on the masks. The network is trained for over 50 million steps if I recall correctly, one game can have max of 81 steps. So it played a lot of games but it's still super weak. I think it's because I trained it vs random bot so it's only learning how to beat random bot. But even that I was surprised that it didn't get to at least 99% vs bot. This is potentially because reward is collected at end of the whole game and there are many actions taken in between so it's quite hard to adjust properly. Vanilla DQN also converges quite slowly, I could potentially try PPO or rainbow DQN. Also implement a better environment for self play instead of constantly playing vs random.

# Video 
[Screencast from 03-10-2024 11:13:04 PM.webm](https://github.com/Algorithm-Arena/weekly-challenge-8-ultimate-tic-tac-toe/assets/32753704/80972c8d-0f4c-45e4-8fd9-ca2415942273)

This is me clicking randomly vs the bot. If I play seriously I can easily beat it. Allowed move for player will show light blue, player won grid will show green, bot won tile will show red, and tied will show yellow

# Installation setup
```
pip install -r requirements.txt
```

# Running the important files
To try to open the game, you just need to run the UI file. 
```
python game_display.py
```
For bench mark run 
```
python benchmark.py
```
For training. You can change the args passed in based on the file like epochs to run
```
python tianshou_train.py 
```
# Files explainations
* agent_play.py The random agent
* benchmark.py The benchmarking vs random bots
* game_display.py The actual UI for playing vs the bot
* game.py The actual execution engine of the game and storing the state. Can make moves and take back. Initially it was designed with efficiency in mind because I was planning to do minimax + backtracking based approach. But initialy implmentation was a bit off in terms of move forcing. After deciding to try RL, I stopped caring about efficiency for updating states and undo
* play.py Make some random moves for the game.py to test it manually
* tianshou_play.py agent for RL based agent
* tianshou_train.py training code
* tianshou_uttt.py training multiagent pettingzoo environment for ultimate tictac toe adapted from tianshou wiki
* uttt_env.py PettingZoo like environment for ultimate tictac toe adapted from regular tic tac toe 
* model/policy.pth trained weights for DQN 
