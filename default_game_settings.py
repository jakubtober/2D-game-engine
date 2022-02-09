import pygame
from pygame import *
import random

from map import Map, MapTile, MiniMap
from game_objects import (
    Character,
    Bird1,
    Cloud,
    Grass,
    Tree,
    PineTree,
    OldTree,
    PieceOfWood,
    Rock,
    Bushes1,
)

pygame.init()
screen_info = pygame.display.Info()

NODE_SIZE = 80
GAME_SCREEN_SIZE = screen_info.current_w, screen_info.current_h
FPS = 60

random_map_matrix = [
    random.choices(
        [
            MapTile(
                is_possible_to_cross=True,
                is_visible=False,
                background_game_object=Grass(),
                fixed_tile_game_object=Grass(),
            ),
            MapTile(
                is_possible_to_cross=False,
                is_visible=False,
                background_game_object=Grass(),
                fixed_tile_game_object=Rock(),
            ),
            MapTile(
                is_possible_to_cross=False,
                is_visible=False,
                background_game_object=Grass(),
                fixed_tile_game_object=Tree(),
            ),
            MapTile(
                is_possible_to_cross=False,
                is_visible=False,
                background_game_object=Grass(),
                fixed_tile_game_object=OldTree(),
            ),
            MapTile(
                is_possible_to_cross=False,
                is_visible=False,
                background_game_object=Grass(),
                fixed_tile_game_object=PineTree(),
            ),
            MapTile(
                is_possible_to_cross=False,
                is_visible=False,
                background_game_object=Grass(),
                fixed_tile_game_object=PieceOfWood(),
            ),
            MapTile(
                is_possible_to_cross=False,
                is_visible=False,
                background_game_object=Grass(),
                fixed_tile_game_object=Bushes1(),
            ),
        ],
        [0.5, 0.03, 0.05, 0.05, 0.05, 0.005, 0.01],
        k=100,
    )
    for row in range(100)
]

# graphic mode init
screen = pygame.display.set_mode(GAME_SCREEN_SIZE, FULLSCREEN, 32)

# clock init
fpsClock = pygame.time.Clock()

# initiate game objects
map = Map(random_map_matrix, 0, 0)
map.draw_whole_map()
mini_map = MiniMap(GAME_SCREEN_SIZE[0] - 101, 1)

my_character = Character(5, 5, map)
my_character.delete_map_shadow_tiles_around()

bird1 = Bird1(3, 3, map)

clouds = [
    Cloud(
        random.randint(0, 700),
        random.randint(0, 700),
        [random.choice(Cloud.cloud_bitmaps)],
    )
    for _ in range(0, 4)
]
dynamic_objects = [my_character, bird1, *clouds]
