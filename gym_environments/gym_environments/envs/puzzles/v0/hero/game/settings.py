# Authors:
# Barreto Luis
# Lezama Luis
# Ramírez Coalbert

from pathlib import Path

import pygame

from .src.frames import generate_frames

TILE_SIZE = 16
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
BOSS_WIDTH = 16
BOSS_HEIGHT = 16

BASE_DIR = Path(__file__).parent

ENVIRONMENT = BASE_DIR / "env.txt"

# Graphics
GAME_TEXTURES = {
    "background": pygame.image.load(BASE_DIR / "graphics" / "background.png"),
    "tiles": pygame.image.load(BASE_DIR / "graphics" / "sheet.png"),
    "main_character": pygame.image.load(BASE_DIR / "graphics" / "main_character.png"),
    "statues": pygame.image.load(BASE_DIR / "graphics" / "statues.png"),
    "floor": pygame.image.load(BASE_DIR / "graphics" / "floor.png"),
    "hero": pygame.image.load(BASE_DIR / "graphics" / "hero.png"),
    "item": pygame.image.load(BASE_DIR / "graphics" / "item.png"),
}

# Initializing the mixer
pygame.mixer.init()

# Loading music
pygame.mixer.music.load(BASE_DIR / "sounds" / "medieval_fantasy.opus")

# Sound effects
SOUNDS = {
    'pickup': pygame.mixer.Sound(BASE_DIR / "sounds" / "power_up.ogg")
}

# Frames
GAME_FRAMES = {
    "tiles": generate_frames(GAME_TEXTURES["tiles"], TILE_SIZE, TILE_SIZE),
    "main_character": generate_frames(
        GAME_TEXTURES["main_character"], PLAYER_WIDTH, PLAYER_HEIGHT
    ),
    "statues": generate_frames(GAME_TEXTURES["statues"], BOSS_WIDTH, BOSS_HEIGHT),
    "floor": generate_frames(GAME_TEXTURES["floor"], TILE_SIZE, TILE_SIZE),
    "hero": generate_frames(GAME_TEXTURES["hero"], TILE_SIZE, TILE_SIZE),
    "item": generate_frames(GAME_TEXTURES["item"], TILE_SIZE, TILE_SIZE),
}
