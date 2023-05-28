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
        self.item_4 = None
        self.item_5 = None
        self.item_6 = None
        self.pickups = 0
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

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.item_4 = Item(x, y, self, "forward")
            self.tile_map.tiles[row][col].busy_by = "IT"

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.item_5 = Item(x, y, self, "forward")
            self.tile_map.tiles[row][col].busy_by = "IT"

            row, col = f.readline().split(" ")
            row, col = int(row), int(col)
            x, y = TileMap.to_screen(row, col)
            self.item_6 = Item(x, y, self, "forward")
            self.tile_map.tiles[row][col].busy_by = "IT"

    def reset(self):
        self.tile_map = None
        self.hero = None
        self.item_1 = None
        self.item_2 = None
        self.item_3 = None
        self.item_4 = None
        self.item_5 = None
        self.item_6 = None
        self.pickups = 0
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

    def check_win(self):
        return self.pickups == 6

    def check_pickup(self):
        mc = self.hero.x, self.hero.y
        i1 = self.item_1.x, self.item_1.y
        i2 = self.item_2.x, self.item_2.y
        i3 = self.item_3.x, self.item_3.y
        i4 = self.item_4.x, self.item_4.y
        i5 = self.item_5.x, self.item_5.y
        i6 = self.item_6.x, self.item_6.y

        if not self.item_1.taken and mc == i1:
            self.item_1.taken = True
            self.pickups += 1
            return True
        if not self.item_2.taken and mc == i2:
            self.item_2.taken = True
            self.pickups += 1
            return True
        if not self.item_3.taken and mc == i3:
            self.item_3.taken = True
            self.pickups += 1
            return True
        if not self.item_4.taken and mc == i4:
            self.item_4.taken = True
            self.pickups += 1
            return True
        if not self.item_5.taken and mc == i5:
            self.item_5.taken = True
            self.pickups += 1
            return True
        if not self.item_6.taken and mc == i6:
            self.item_6.taken = True
            self.pickups += 1
            return True

        return False

    def get_state(self):
        mc_i, mc_j = TileMap.to_map(self.hero.x, self.hero.y)
        mc_p = mc_i * self.tile_map.cols + mc_j

        it_p = ((not self.item_1.taken) |
                (not self.item_2.taken) << 1 |
                (not self.item_3.taken) << 2 |
                (not self.item_1.taken) << 3 |
                (not self.item_2.taken) << 4 |
                (not self.item_3.taken) << 5)
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
        if not self.item_4.taken:
            self.item_4.render(surface)
        if not self.item_5.taken:
            self.item_5.render(surface)
        if not self.item_6.taken:
            self.item_6.render(surface)
        self.hero.render(surface)
