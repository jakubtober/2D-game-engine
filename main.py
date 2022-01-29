import sys, pygame, random, constants
from help_functions import node_info
from pygame.locals import *
from game_objects import Character, Cloud
from map import MapTile, Map, MiniMap


map = [
    random.choices(
        [MapTile(0, False), MapTile(1, False), MapTile(2, False), MapTile(3, False)], [0.7, 0.01, 0.1, 0.001], k=100
    )
    for row in range(100)
]
map_rows = len(map)
map_columns = len(map[0])

# graphic mode init
screen = pygame.display.set_mode(constants.GAME_SCREEN_SIZE, FULLSCREEN, 32)

# clock init
fpsClock = pygame.time.Clock()

# initiate game objects
map = Map(map, 0, 0)
map.draw_whole_map()
mini_map = MiniMap(map, constants.GAME_SCREEN_SIZE[0] - 100, 0)

my_character = Character('knight', 5, 5, map)
Cloud.generate_clouds()

#  Main game loop
while True:
    print(fpsClock)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not my_character.is_moving:
            clicked_node = node_info(mouse_pos)
            my_character.end_node = (
                clicked_node[0] + map.first_node_row,
                clicked_node[1] + map.first_node_column
            )
            my_character.start_node = my_character.actual_node(map)

            my_character.path = my_character.find_path(
                map,
                my_character.start_node,
                my_character.end_node
            )

            if my_character.path:
                my_character.is_moving = True

        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT) or (mouse_pos[0] > constants.GAME_SCREEN_SIZE[0] - 40):
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
            if (mouse_pos[0] > constants.GAME_SCREEN_SIZE[0] - 40):
                if map.first_node_column < map.map_columns - 10:
                    map.first_node_column += 1
                    my_character.update_map_movement_position(1, 0)
            elif (mouse_pos[0] < 40):
                if map.first_node_column > 0:
                    map.first_node_column -= 1
                    my_character.update_map_movement_position(-1, 0)
            elif (mouse_pos[1] < 40):
                if map.first_node_row > 0:
                    map.first_node_row -= 1
                    my_character.update_map_movement_position(0, -1)
            elif (mouse_pos[1] > constants.GAME_SCREEN_SIZE[1] - 40):
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

    fpsClock.tick(constants.FPS)
