import sys, pygame, time, random
from help_functions import node_info
from pygame.locals import *
from game_objects import Map, GameObject, Character, Cloud



test_map = [[0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 3, 0, 1, 1, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 2, 2, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]

map_rows = len(test_map)
map_columns = len(test_map[0])

# graphic mode init
pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size, 0, 32)

FPS = 60
fpsClock = pygame.time.Clock()


map = Map(test_map, 1, 1)
my_character = Character('knight', 5, 5)
cloud1 = Cloud(
    'cloud',
    random.randint(0, 600),
    random.randint(100, 600),
    pygame.image.load("./img/cloud1.png")
)
cloud2 = Cloud(
    'cloud',
    random.randint(0, 600),
    random.randint(100, 600),
    pygame.image.load("./img/cloud2.png")
)


#  Main game loop
while True:
    # print(fpsClock)
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not my_character.is_moving:
        my_character.end_node = node_info(pygame.mouse.get_pos())
        my_character.start_node = my_character.node
        my_character.end_node = my_character.end_node
        my_character.path = my_character.find_and_draw_path(
            screen,
            map.visible_map,
            my_character.start_node,
            my_character.end_node
        )

        if my_character.path:
            my_character.is_moving = True

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            if map.first_node_column < map_columns - 10:
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
            if map.first_node_row < map_rows - 10:
                map.first_node_row += 1
                my_character.update_map_movement_position(0, 1)

    if my_character.is_moving:
        my_character.move()

    map.draw(screen)
    my_character.draw(screen)
    cloud1.draw(screen)
    cloud2.draw(screen)
    pygame.display.update()

    fpsClock.tick(FPS)
