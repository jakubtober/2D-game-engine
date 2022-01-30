import pygame
from pygame import *
import random
from map import Map, MapTile, MiniMap
from game_objects import Character, Cloud

pygame.init()
screen_info = pygame.display.Info()

NODE_SIZE = 80
GAME_SCREEN_SIZE = screen_info.current_w, screen_info.current_h
FPS = 70

random_map_matrix = [
    random.choices(
        [
            MapTile("grass", False),
            MapTile("rock", False),
            MapTile("tree", False),
            MapTile("house", False),
        ],
        [0.7, 0.01, 0.1, 0.001],
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
mini_map = MiniMap(GAME_SCREEN_SIZE[0] - 100, 0)

my_character = Character("knight", 5, 5, map)
Cloud.generate_clouds()
