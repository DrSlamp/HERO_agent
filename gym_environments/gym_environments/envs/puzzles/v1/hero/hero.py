# Authors:
# Barreto Paul
# Lezama Luis
# Ramírez Coalbert

import time

import numpy as np

import pygame

import gym
from gym import spaces

from .game.Game import Game
from .game import settings


class HeroEnv(gym.Env):
    metadata = {"render_modes": ["human","training"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()
        self.render_mode = kwargs.get("render_mode")
        self.game = Game("Hero Env", self.render_mode)
        self.n = self.game.world.tile_map.rows * self.game.world.tile_map.cols
        # # [row, col, taken_item_1, taken_item_2, taken_item_3, ]
        # self.low = np.array([0.0, 0.0, 0, 0, 0], dtype=np.float32)
        # self.high = np.array([np.inf, np.inf, 1, 1, 1], dtype=np.float32)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(self.n * self.n * self.n)
        # self.observation_space = spaces.Box(self.low, self.high, dtype=np.float32)

        self.current_state = self.game.get_state()
        self.current_action = 0
        self.current_reward = 0.0
        self.pickups = 0
        self.delay = 0.07

    def __compute_state_result(self, mc, it, bs):
        # print(f"new state is MC:{mc}, it:{it}, state:{it * self.n + mc}")
        return bs * self.n**2 + it * self.n + mc

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get("delay", 0.07)

        np.random.seed(seed)

        self.current_state = self.game.reset()
        self.current_action = 0
        self.current_reward = 0
        self.pickups = 0

        # return np.array(self.current_state, dtype==np.float32), {}
        return self.__compute_state_result(*self.current_state), {}

    def step(self, action):
        self.current_action = action
        
        terminated = False
        self.current_reward = -15 + self.game.world.pickups*2

        old_state = self.current_state
        self.current_state = self.game.update(self.current_action)

        if old_state == self.current_state:
            self.current_reward = -30.0
        elif self.game.world.check_lost():
            self.current_reward = -1000
            self.terminated = True
        if self.game.world.pickups == 5:
            if self.render_mode == "human":
                settings.SOUNDS['pickup'].play()

            self.current_reward = 1000
            terminated = True

        # if self.render_mode == "training":
        #     self.render()
        #     time.sleep(0.0005)
        elif self.render_mode == "human":
            self.render()
            time.sleep(0.4)

        return (
            self.__compute_state_result(*self.current_state),
            self.current_reward,
            terminated,
            False,
            {},
        )

    def render(self):
        self.game.render()

    def close(self):
        self.game.close()
