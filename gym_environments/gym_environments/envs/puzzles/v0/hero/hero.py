# Authors:
# Barreto Luis
# Lezama Luis
# Ramírez Coalbert

import time

import numpy as np

import pygame

import gym
from gym import spaces

from .game.Game import Game


class HeroEnv(gym.Env):
    metadata = {"render_modes": ["human","training"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()
        self.render_mode = kwargs.get("render_mode")
        self.game = Game("Hero Env", self.render_mode)
        self.n = self.game.world.tile_map.rows * self.game.world.tile_map.cols
        self.observation_space = spaces.Discrete(self.n * self.n)
        self.action_space = spaces.Discrete(4)
        self.current_state = self.game.get_state()
        self.current_action = 0
        self.current_reward = 0.0
        self.pickups = 0
        self.delay = 0.07

    def __compute_state_result(self, mc, it):
        return mc * self.n + it

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

        return self.__compute_state_result(*self.current_state), {}

    def step(self, action):
        self.current_action = action
        
        terminated = False
        self.current_reward = -2.0

        if self.game.world.check_collision():
            self.pickups += 1
            print (f"{self.pickups} ", end='')
            self.current_reward = self.pickups * 1000.0
            if self.pickups == 3:
                print("")
                terminated = True
        
        old_state = self.current_state
        self.current_state = self.game.update(self.current_action)

        if old_state == self.current_state:
            self.current_reward = -20.0

        if self.render_mode is "training":
            self.render()
            time.sleep(0.5)
        elif self.render_mode is "human":
            self.render()
            time.sleep(0.5)

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
