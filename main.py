import sys
import pygame
from pygame.locals import *

from default_game_settings import (
    my_character,
    fpsClock,
    FPS,
    GAME_SCREEN_SIZE,
    map,
    screen,
    mini_map,
    clouds, bird1,
)
from game_objects import Cloud
from help_functions import tile_row_and_column


#  Main game loop
while True:
    print(fpsClock)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and not my_character.is_moving
        ):
            clicked_map_tile_row_and_column = tile_row_and_column(mouse_pos)
            my_character.path_end_tile = (
                clicked_map_tile_row_and_column[0]
                + map.row_index_of_first_visible_tile,
                clicked_map_tile_row_and_column[1]
                + map.column_index_of_first_visible_tile,
            )
            my_character.start_tile = my_character.actual_row_and_column_index(map)

            my_character.path = my_character.find_path(
                map, my_character.start_tile, my_character.path_end_tile
            )

            if my_character.path:
                my_character.is_moving = True

        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT) or (
                mouse_pos[0] > GAME_SCREEN_SIZE[0] - 40
            ):
                if map.column_index_of_first_visible_tile < map.map_columns - 10:
                    map.column_index_of_first_visible_tile += 1
                    my_character.update_map_movement_position(1, 0)
            elif event.key == pygame.K_LEFT:
                if map.column_index_of_first_visible_tile > 0:
                    map.column_index_of_first_visible_tile -= 1
                    my_character.update_map_movement_position(-1, 0)
            elif event.key == pygame.K_UP:
                if map.row_index_of_first_visible_tile > 0:
                    map.row_index_of_first_visible_tile -= 1
                    my_character.update_map_movement_position(0, -1)
            elif event.key == pygame.K_DOWN:
                if map.row_index_of_first_visible_tile < map.map_rows - 10:
                    map.row_index_of_first_visible_tile += 1
                    my_character.update_map_movement_position(0, 1)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            if mouse_pos[0] > GAME_SCREEN_SIZE[0] - 40:
                if map.column_index_of_first_visible_tile < map.map_columns - 10:
                    map.column_index_of_first_visible_tile += 1
                    my_character.update_map_movement_position(1, 0)
            elif mouse_pos[0] < 40:
                if map.column_index_of_first_visible_tile > 0:
                    map.column_index_of_first_visible_tile -= 1
                    my_character.update_map_movement_position(-1, 0)
            elif mouse_pos[1] < 40:
                if map.row_index_of_first_visible_tile > 0:
                    map.row_index_of_first_visible_tile -= 1
                    my_character.update_map_movement_position(0, -1)
            elif mouse_pos[1] > GAME_SCREEN_SIZE[1] - 40:
                if map.row_index_of_first_visible_tile < map.map_rows - 10:
                    map.row_index_of_first_visible_tile += 1
                    my_character.update_map_movement_position(0, 1)

    if my_character.is_moving:
        my_character.move()
        my_character.update_map_shadow_tiles_around()

    map.display_visible_map_surface(screen)
    my_character.draw(screen)
    bird1.draw(screen)

    for cloud in clouds:
        cloud.draw(screen)

    mini_map.draw(screen, map, my_character)

    pygame.display.update()

    fpsClock.tick(FPS)
