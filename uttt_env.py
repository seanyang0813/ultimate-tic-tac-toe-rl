# modified from regular tic tac toe set up in petting zoo
# noqa: D212, D415

from __future__ import annotations

import os

import gymnasium
import numpy as np
from gymnasium import spaces
from gymnasium.utils import EzPickle

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers
from game import Game, Player


def env(render_mode=None):
    internal_render_mode = "log"
    env = raw_env(render_mode=internal_render_mode)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(AECEnv, EzPickle):
    metadata = {
        "render_modes": ["log"],
        "name": "ultimate-tic-tac-toe",
        "is_parallelizable": False
    }

    def __init__(
        self, render_mode: str | None = None, screen_height: int | None = 1000
    ):
        super().__init__()
        EzPickle.__init__(self, render_mode, screen_height)
        self.board = Game()

        self.agents = ["player_1", "player_2"]
        self.possible_agents = self.agents[:]

        self.action_spaces = {i: spaces.Discrete(81) for i in self.agents}
        self.observation_spaces = {
            i: spaces.Dict(
                {
                    "observation": spaces.Box(
                        low=0, high=1, shape=(9, 9, 2), dtype=np.int8
                    ),
                    "action_mask": spaces.Box(low=0, high=1, shape=(81,), dtype=np.int8),
                }
            )
            for i in self.agents
        }

        self.rewards = {i: 0 for i in self.agents}
        self.terminations = {i: False for i in self.agents}
        self.truncations = {i: False for i in self.agents}
        self.infos = {i: {"legal_moves": list(range(0, 81))} for i in self.agents}

        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()

        self.render_mode = render_mode
        self.screen_height = screen_height
        self.screen = None

    def observe(self, agent):
        observation = self.board.convert_board_to_np_array()
        legal_moves = sorted(self.board.get_all_valid_moves() if agent == self.agent_selection else [])
        action_mask = np.zeros(81, "int8")
        for (x, y) in legal_moves:
            action_mask[y * 9 + x] = 1
        return {"observation": observation, "action_mask": action_mask}


    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]


    # action in this case is a value from 0 to 8 indicating position to move on tictactoe board

    def step(self, action):
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            return self._was_dead_step(action)
        assert self.board.is_move_allowed(action % 9 , action // 9)
        # takes in x and y coordinates of the square to move to
        self.board.make_move(action % 9, action // 9)

        # update infos
        # list of valid actions (indexes in board)
        # next_agent = self.agents[(self.agents.index(self.agent_selection) + 1) % len(self.agents)]
        next_agent = self._agent_selector.next()
        (won, player) = self.board.is_game_over_and_winner()

        if won:
            winner = player
            if winner == Player.EMPTY:
                # tie
                pass
            elif player == Player.X:
                # agent 0 won because it's always the first to go
                self.rewards[self.agents[0]] += 1
                self.rewards[self.agents[1]] -= 1
            else:
                # agent 1 won
                self.rewards[self.agents[1]] += 1
                self.rewards[self.agents[0]] -= 1
            # once either play wins or there is a draw, game over, both players are done
            self.terminations = {i: True for i in self.agents}


        # Switch selection to next agents
        self._cumulative_rewards[self.agent_selection] = 0
        self.agent_selection = next_agent
        self._accumulate_rewards()
    


    def reset(self, seed=None, options=None):
        # reset environment
        self.board = Game()

        self.agents = self.possible_agents[:]
        self.rewards = {i: 0 for i in self.agents}
        self._cumulative_rewards = {i: 0 for i in self.agents}
        self.terminations = {i: False for i in self.agents}
        self.truncations = {i: False for i in self.agents}
        self.infos = {i: {} for i in self.agents}
        # selects the first agent
        self._agent_selector.reinit(self.agents)
        self._agent_selector.reset()
        self.agent_selection = self._agent_selector.reset()

 
    def close(self):
        pass

    def render(self):
        self.board.print_board()
