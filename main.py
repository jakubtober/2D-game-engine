import sys, pygame
from default_game_settings import (
    my_character,
    fpsClock,
    FPS,
    GAME_SCREEN_SIZE,
    map,
    screen,
    mini_map,
)
from game_objects import Cloud
from help_functions import node_info
from pygame.locals import *


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
            clicked_node = node_info(mouse_pos)
            my_character.end_node = (
                clicked_node[0] + map.first_node_row,
                clicked_node[1] + map.first_node_column,
            )
            my_character.start_node = my_character.actual_node(map)

            my_character.path = my_character.find_path(
                map, my_character.start_node, my_character.end_node
            )

            if my_character.path:
                my_character.is_moving = True

        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT) or (
                mouse_pos[0] > GAME_SCREEN_SIZE[0] - 40
            ):
                if map.first_node_column < map.map_columns - 10:
                    map.first_node_column += 1
                    my_character.update_map_movement_position(1, 0)
            elif event.key == pygame.K_LEFT:
                if map.first_node_column > 0:
                    map.first_node_column -= 1
                    my_character.update_map_movement_position(-1, 0)
            elif event.key == pygame.K_UP:
                if map.first_node_row > 0:
                    map.first_node_row -= 1
                    my_character.update_map_movement_position(0, -1)
            elif event.key == pygame.K_DOWN:
                if map.first_node_row < map.map_rows - 10:
                    map.first_node_row += 1
                    my_character.update_map_movement_position(0, 1)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            if mouse_pos[0] > GAME_SCREEN_SIZE[0] - 40:
                if map.first_node_column < map.map_columns - 10:
                    map.first_node_column += 1
                    my_character.update_map_movement_position(1, 0)
            elif mouse_pos[0] < 40:
                if map.first_node_column > 0:
                    map.first_node_column -= 1
                    my_character.update_map_movement_position(-1, 0)
            elif mouse_pos[1] < 40:
                if map.first_node_row > 0:
                    map.first_node_row -= 1
                    my_character.update_map_movement_position(0, -1)
            elif mouse_pos[1] > GAME_SCREEN_SIZE[1] - 40:
                if map.first_node_row < map.map_rows - 10:
                    map.first_node_row += 1
                    my_character.update_map_movement_position(0, 1)

    if my_character.is_moving:
        my_character.move(map)
        my_character.update_map_shadow_tiles_around(map)

    map.display_visible_map_surface(screen)
    my_character.draw(screen, map)

    Cloud.draw_clouds(screen)
    mini_map.draw(screen, map, my_character)

    pygame.display.update()

    fpsClock.tick(FPS)
