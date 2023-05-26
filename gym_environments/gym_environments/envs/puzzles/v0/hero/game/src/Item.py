# Authors:
# Barreto Luis
# Lezama Luis
# Ramírez Coalbert

from .. import settings

from .Entity import Entity


class Item(Entity):
    def __init__(self, x, y, game_level, movement_direction):
        super().__init__(
            x,
            y,
            settings.BOSS_WIDTH,
            settings.BOSS_HEIGHT,
            "item",
            0,
            game_level,
            {
                0: self.move_left,
                1: self.move_down,
                2: self.move_right,
                3: self.move_up,
            },
            "IT",
        )
        self.movement_direction = movement_direction

    def undo_movement(self):
        self.off_set_i *= -1
        self.off_set_j *= -1
        self.move()

    def on_player_movement(self, action):
        self.movement[action]()
