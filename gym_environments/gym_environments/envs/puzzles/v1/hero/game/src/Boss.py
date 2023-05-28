# Authors:
# Barreto Paul
# Lezama Luis
# Ramírez Coalbert

from .. import settings

from .Entity import Entity


class Boss(Entity):
    def __init__(self, x, y, game_level, movement_direction):
        super().__init__(
            x,
            y,
            settings.BOSS_WIDTH,
            settings.BOSS_HEIGHT,
            "boss",
            9,
            game_level,
            {
                0: self.move_left,
                1: self.move_down,
                2: self.move_right,
                3: self.move_up,
            },
            "BS",
        )
        self.off_set_j = -1
        self.movement_direction = movement_direction

    def act(self):
        if (self.x//16 == 6) or (self.x//16 == 2):
            self.off_set_j *= -1
        self.frame_index = 9 + (self.frame_index + 1)%3
        self.move()

    def undo_movement(self):
        self.off_set_i *= -1
        self.off_set_j *= -1
        self.move()

    def on_player_movement(self, action):
        self.movement[action]()
