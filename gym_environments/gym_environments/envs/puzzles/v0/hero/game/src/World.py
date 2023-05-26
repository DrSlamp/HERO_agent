# Authors:
# Barreto Luis
# Lezama Luis
# Ramírez Coalbert

from .. import settings

from .Tilemap import Tile, TileMap
from .Hero import Hero
from .Boss import Boss
from .Item import Item

import random

TILES = {"0": {"frame": 4}, "1": {"frame": 0}, "2": {"frame": 3}}


class World:
    def __init__(self):
        self.tile_map = None
        self.hero = None
        self.item_1 = None
        self.item_2 = None
        self.item_3 = None
        # self.statue_1 = None
        # self.statue_2 = None
        # self.target_1 = None
        # self.target_2 = None
        self.__load_environment()

    def __load_environment(self) -> None:
        with open(settings.ENVIRONMENT, "r") as f:
            rows, cols = f.readline().split(" ")
            rows, cols = int(rows), int(cols)
            self.tile_map = TileMap(rows, cols)

            for i in range(rows):
                row = f.readline()
                if row[-1] == "\n":
                    row = row[:-1]
                row = row.split(" ")

                for j in range(cols):
                    tile_def = TILES[row[j]]
                    x, y = TileMap.to_screen(i, j)
                    if tile_def == {"frame": 0}:
                        rnd = random.randint(0,2)
                        self.tile_map.tiles[i][j] = Tile(x, y, rnd)
                        self.tile_map.map[i][j] = int(row[j])    
                    else:
                        self.tile_map.tiles[i][j] = Tile(x, y, tile_def["frame"])
                        self.tile_map.map[i][j] = int(row[j])

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.hero = Hero(x, y, self)
            self.tile_map.tiles[row][col].busy_by = "HR"

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.item_1 = Item(x, y, self, "forward")
            self.tile_map.tiles[row][col].busy_by = "IT"

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.item_2 = Item(x, y, self, "forward")
            self.tile_map.tiles[row][col].busy_by = "IT"

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.item_3 = Item(x, y, self, "forward")
            self.tile_map.tiles[row][col].busy_by = "IT"

            # row, col = f.readline().split(" ")
            # self.target_1 = int(row), int(col)

            # row, col = f.readline().split(" ")
            # self.target_2 = int(row), int(col)

    def reset(self):
        self.tile_map = None
        self.hero = None
        self.item_1 = None
        self.item_2 = None
        self.item_3 = None
        self.__load_environment()
        return self.get_state()

    def check_lost(self) -> None:
        return False
        # return (
        #     self.hero.x == self.statue_1.x
        #     and self.hero.y == self.statue_1.y
        # ) or (
        #     self.hero.x == self.statue_2.x
        #     and self.hero.y == self.statue_2.y
        # )

    def check_win(self, pickups):
        return pickups == 3

    def check_collision(self):
        mc = self.hero.x, self.hero.y
        ans = False
        if self.item_1.taken is not None:
            i1 = self.item_1.x, self.item_1.y
            # if (mc == i1):
            #     print(f"collided with i1")
            ans = (mc == i1)
        if self.item_2.taken is not None:
            i2 = self.item_2.x, self.item_2.y
            # if (mc == i2):
            #     print(f"collided with i2")
            ans = (mc == i2)
        if self.item_3.taken is not None:
            i3 = self.item_3.x, self.item_3.y
            # if (mc == i3):
            #     print(f"collided with i3")
            ans = (mc == i3)

        return ans

    def check_pickup(self):
        mc = self.hero.x, self.hero.y
        if not self.item_1.taken:
            i1 = self.item_1.x, self.item_1.y
            if mc == i1:
                self.item_1.taken = True
                return True
        if not self.item_2.taken:
            i2 = self.item_2.x, self.item_2.y
            if mc == i2:
                self.item_2.taken = True
                return True
        if not self.item_3.taken:
            i3 = self.item_3.x, self.item_3.y
            if mc == i3:
                self.item_3.taken = True
                return True

        return False

    def get_state(self):
        mc_i, mc_j = TileMap.to_map(self.hero.x, self.hero.y)
        mc_p = mc_i * self.tile_map.cols + mc_j

        it_p = ((self.item_1 is not None) +
                (self.item_2 is not None) << 1 +
                (self.item_3 is not None) << 2)

        return [mc_p, it_p]

    def apply_action(self, action):
        self.hero.act(action)
        self.check_pickup()

        mc, it = self.get_state()

        return mc, it

    def render(self, surface):
        surface.blit(settings.GAME_TEXTURES["background"], (0, 0))
        self.tile_map.render(surface)
        if not self.item_1.taken:
            self.item_1.render(surface)
        if not self.item_2.taken:
            self.item_2.render(surface)
        if not self.item_3.taken:
            self.item_3.render(surface)
        self.hero.render(surface)
