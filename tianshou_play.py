
from tianshou.utils.net.common import Net
from tianshou.policy import DQNPolicy
from tianshou.data import Batch
import torch
from game import Game

game = Game()
test = [False for x in range(81)]
test[3] = True
batch = Batch(obs= [{'agent_id': 1, 'obs': game.convert_board_to_np_array(), 'mask': test, 
                     }], info=None)

class RLAgent:
    def __init__(self):
        state_shape = (9, 9, 2)
        action_shape = 81
        hidden_sizes = [128, 128, 128, 128]
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        net = Net(
            state_shape,
            action_shape,
            hidden_sizes=hidden_sizes,
            device=device,
        ).to(device)
        optim = torch.optim.Adam(net.parameters(), lr=0.0001)
        agent_learn = DQNPolicy(
            model=net,
            optim=optim,
            action_space=action_shape,
            estimation_step=3,
            discount_factor=0.9,
            target_update_freq=320,
        )
        agent_learn.load_state_dict(torch.load("./model/policy.pth"))
        self.agent = agent_learn
    
    def play_move(self, game: Game):
        mask = [False for x in range(81)]
        for move in  game.get_all_valid_moves():
            mask[move[0] + move[1] * 9] = True
        batch = Batch(obs= [{'agent_id': 1, 'obs': game.convert_board_to_np_array(), 'mask': mask
                             }], info=None)
        res = self.agent.forward(batch)
        res = res.act[0]
        move = (res % 9, res // 9)
        game.make_move(move[0], move[1])
