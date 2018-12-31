import sys, pygame, time
import random
from pygame.locals import *
from apath import astar
import threading
from help_functions import node_info



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


class GameObject():
    def __init__(self, object_type, x, y, img):
        self.object_type = object_type
        self.x = x
        self.y = y
        self.img = img

    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        self.x += 1
        if self.x == 800:
            self.x = -100
            self.y = random.randint(100, 700)


class Map():
    def __init__(self, map, first_node_row, first_node_column):
        self.first_node_column = first_node_column
        self.first_node_row = first_node_row
        self.map = map

    @property
    def visible_map(self):
        sliced_rows = self.map[self.first_node_row:]
        visible_map = [row[self.first_node_column:] for row in sliced_rows]
        return visible_map


    def draw(self):
        visible_map_width = 10
        map_elements_number = visible_map_width * 10

        font = pygame.font.SysFont('Comic Sans MS', 20)
        grass = pygame.image.load("./img/grass.jpg")
        rock = pygame.image.load("./img/rock.png")
        tree2 = pygame.image.load("./img/tree2.png")
        house1 = pygame.image.load("./img/house1.png")

        for node_number in range(map_elements_number):
            # divmod(a, b)
            # (a // b, a % b)
            node_column, node_row = divmod(node_number, 10)

            x = (node_column) * 80
            y = (node_row) * 80
            textsurface = font.render(f'{node_number}', True, (255, 255, 255))

            screen.blit(grass, (x, y))

            if self.visible_map[node_row][node_column] == 1:
                screen.blit(rock, (x, y))
            elif self.visible_map[node_row][node_column] == 2:
                screen.blit(tree2, (x, y))
            elif self.visible_map[node_row][node_column] == 3:
                screen.blit(house1, (x, y))

        # draw yellow border around node that is pointed by the mouse
        node = node_info(pygame.mouse.get_pos())
        rect_x = node[1] * 80
        rect_y = node[0] * 80
        pygame.draw.rect(screen, (255, 255, 0), (rect_x, rect_y, 80, 80), 1)

class Character():
    def __init__(self, type, node_x, node_y):
        self.type = type
        self.x = node_x * 80
        self.y = node_y * 80
        self.node_column = self.x // 80
        self.node_row = self.y // 80
        self.is_moving = False
        self.start_node = (node_y // 80, node_x // 80)
        self.end_node = ()
        self.path = []
        self.direction = 'E'

        if self.type == 'knight':
            self.character_east = pygame.image.load('./img/knight_east.png')
            self.character_west = pygame.image.load('./img/knight_west.png')

    @property
    def node(self):
        return (self.y // 80, self.x // 80)

    def draw(self):
        if self.direction == 'E':
            screen.blit(self.character_east, (self.x, self.y))
        elif self.direction == 'W':
            screen.blit(self.character_west, (self.x, self.y))

        if self.is_moving:
            pygame.draw.circle(
                screen,
                (200, 0, 0),
                ((self.end_node[1] * 80) + 40 , (self.end_node[0] * 80) + 40),
                20,
                3
            )

    def move(self):
            if self.is_moving:
                if (self.end_node[1] * 80 == self.x) and (self.end_node[0] * 80 == self.y):
                    self.is_moving = False
                else:
                    if (self.path[1][1] * 80 == self.x) and (self.path[1][0] * 80 == self.y):
                        self.path[1] = self.node
                        self.path.pop(0)
                    else:
                        if (self.path[1][1] * 80 - self.x) < 0:
                            self.x -= 1
                            self.direction = 'W'
                        elif (self.path[1][1] *80 - self.x) > 0:
                            self.x += 1
                            self.direction = 'E'
                        if (self.path[1][0] * 80 - self.y) < 0:
                            self.y -= 1
                        elif (self.path[1][0] *80 - self.y) > 0:
                            self.y += 1

    def draw_path(self, path):
        for node in path:
            if path.index(node) < (len(path) - 1):
                next_node = path[path.index(node) + 1]
                pygame.draw.line(
                    screen,
                    (255, 255, 0),
                    ((node[1] * 80) + 40, (node[0] * 80) + 40),
                    ((next_node[1] * 80) + 40, (next_node[0] * 80) + 40),
                    3)
                pygame.display.update()

    def find_and_draw_path(self, test_map, start_node, end_node):
        start_node_not_obsticle = (test_map[start_node[0]][start_node[1]] != 1)
        end_node_not_obsticle = (test_map[end_node[0]][end_node[1]] != 1)

        if start_node_not_obsticle and end_node_not_obsticle:
            path = astar(test_map, start_node, end_node)
            if path:
                self.draw_path(path)
                return path

    def update_map_movement_position(self, node_column_change, node_row_change):
        my_character.x += 80 * (node_column_change * (-1))
        my_character.y += 80 * (node_row_change * (-1))
        my_character.start_node = (
            my_character.start_node[0] + (node_row_change * (-1)),
            my_character.start_node[1] + (node_column_change * (-1)),
        )
        if self.is_moving:
            my_character.end_node = (
                my_character.end_node[0] + (node_row_change * (-1)),
                my_character.end_node[1] + (node_column_change * (-1)),
            )
            self.path = [(node[0] + (node_row_change * (-1)), node[1] + (node_column_change * (-1))) for node in self.path]


map = Map(test_map, 1, 1)
my_character = Character('knight', 5, 5)
cloud1 = GameObject('cloud', random.randint(0, 600), random.randint(100, 600), pygame.image.load("./img/cloud1.png"))
cloud2 = GameObject('cloud', random.randint(0, 600), random.randint(100, 600), pygame.image.load("./img/cloud2.png"))


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

    map.draw()
    my_character.draw()
    cloud1.draw()
    cloud2.draw()
    pygame.display.update()


    fpsClock.tick(FPS)
