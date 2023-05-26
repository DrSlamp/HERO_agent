# Authors:
# Barreto Luis
# Lezama Luis
# Ramírez Coalbert

from typing import TypeVar

from .. import settings

from .Entity import Entity


class Hero(Entity):
    def __init__(self, x, y, world):
        super().__init__(
            x,
            y,
            settings.PLAYER_WIDTH,
            settings.PLAYER_HEIGHT,
            "hero",
            1,
            world,
            {0: self.move_left, 1: self.move_down, 2: self.move_right, 3: self.move_up},
            "HR",
        )
        # Frames by action
        # self.frames = [10, 7, 4, 1]
        self.frames = [4, 0, 12, 8]

    def act(self, action):
        self.movement[action]()
        self.frame_index = self.frames[action]
