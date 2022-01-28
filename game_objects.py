import sys, pygame, time, random, constants
from pygame.locals import *
from apath import astar, MAP_OBSTACLES

from help_functions import (node_info,
    global_column_to_local_x_coordinate,
    global_row_to_local_y_coordinate
)


class GameObject():
    objects_list = []

    def __init__(self, object_type, x, y, img=None):
        self.object_type = object_type
        self.objects_list.append(self)
        self.x = x
        self.y = y
        self.img = img

    def actual_node(self, map):
        actual_node_column = map.first_node_column + (self.x // constants.NODE_SIZE)
        actual_node_row = map.first_node_row + (self.y // constants.NODE_SIZE)
        return (actual_node_row, actual_node_column)

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.x, self.y))


class Character(GameObject):
    def __init__(self, object_type, node_x, node_y, map):
        GameObject.__init__(self, 'knight', node_x * constants.NODE_SIZE, node_y * constants.NODE_SIZE)
        self.node_column = self.x // constants.NODE_SIZE
        self.node_row = self.y // constants.NODE_SIZE

        self.start_node = (node_y // constants.NODE_SIZE, node_x // constants.NODE_SIZE)
        self.end_node = ()

        self.is_moving = False
        self.path = []
        self.direction = 'E'

        self.character_east = pygame.image.load('./img/knight_east.png')
        self.character_west = pygame.image.load('./img/knight_west.png')
        self.update_map_shadow_tiles_around(map)

    def map_node(self, map):
        return (
            map.first_node_row + (self.y // constants.NODE_SIZE),
            map.first_node_column + (self.x // constants.NODE_SIZE)
        )

    def update_map_shadow_tiles_around(self, map):
        actual_character_node = self.actual_node(map)
        for tile_row_to_update in range(actual_character_node[0] - 3, actual_character_node[0] + 4):
            for tile_column_to_update in range(actual_character_node[1] - 3, actual_character_node[1] + 4):
                map.update_shadow_map_tile(tile_row_to_update, tile_column_to_update)

    def draw(self, screen, map):
        if self.direction == 'E':
            screen.blit(self.character_east, (self.x, self.y))
        elif self.direction == 'W':
            screen.blit(self.character_west, (self.x, self.y))

        if self.is_moving:
            circle_x = (
                global_column_to_local_x_coordinate(map, (self.end_node[1])) + 40
            )
            circle_y = (
                global_row_to_local_y_coordinate(map, (self.end_node[0])) + 40
            )

            pygame.draw.circle(
                screen,
                (200, 0, 0),
                (circle_x , circle_y),
                constants.NODE_SIZE // 4,
                3
            )

    def move(self, map):
        end_node_x_is_self_x = (
            global_column_to_local_x_coordinate(map, self.end_node[1]) == self.x
        )
        end_node_y_is_self_y = (
            global_row_to_local_y_coordinate(map, self.end_node[0]) == self.y
        )
        second_path_node_x_is_self_x = (
            global_column_to_local_x_coordinate(map, self.path[1][1]) == self.x
        )
        second_path_node_y_is_self_y = (
            global_row_to_local_y_coordinate(map, self.path[1][0]) == self.y
        )

        if self.is_moving:
            if end_node_x_is_self_x and end_node_y_is_self_y:
                self.is_moving = False
            else:
                if second_path_node_x_is_self_x and second_path_node_y_is_self_y:
                    self.path[1] = self.map_node(map)
                    self.path.pop(0)
                else:
                    if (global_column_to_local_x_coordinate(map, self.path[1][1]) - self.x) < 0:
                        self.x -= 1
                        self.direction = 'W'
                    elif (global_column_to_local_x_coordinate(map, self.path[1][1]) - self.x) > 0:
                        self.x += 1
                        self.direction = 'E'
                    if (global_row_to_local_y_coordinate(map, self.path[1][0]) - self.y) < 0:
                        self.y -= 1
                    elif (global_row_to_local_y_coordinate(map, self.path[1][0]) - self.y) > 0:
                        self.y += 1

    def draw_path(self, screen, path):
        for node in path:
            if path.index(node) < (len(path) - 1):
                next_node = path[path.index(node) + 1]
                pygame.draw.line(
                    screen,
                    (255, 255, 0),
                    ((node[1] * constants.NODE_SIZE) + 40, (node[0] * constants.NODE_SIZE) + 40),
                    ((next_node[1] * constants.NODE_SIZE) + 40, (next_node[0] * constants.NODE_SIZE) + 40),
                    3)

    def find_path(self, map, start_node, end_node):
        start_node_not_obsticle = (map.map[start_node[0]][start_node[1]].tile_type not in MAP_OBSTACLES)
        end_node_not_obsticle = (map.map[end_node[0]][end_node[1]].tile_type not in MAP_OBSTACLES)

        if start_node_not_obsticle and end_node_not_obsticle:
            path = astar(map.map, start_node, end_node)
            if path:
                return path

    def update_map_movement_position(self, node_column_change, node_row_change):
        self.x += constants.NODE_SIZE * (node_column_change * (-1))
        self.y += constants.NODE_SIZE * (node_row_change * (-1))


class Cloud(GameObject):
    clouds_list = []
    cloud_images = [
        pygame.image.load("./img/cloud1.png"),
        pygame.image.load("./img/cloud2.png"),
        pygame.image.load("./img/cloud3.png"),
        pygame.image.load("./img/cloud4.png"),
    ]

    def __init__(self, x, y, img):
        GameObject.__init__(self, 'cloud', x, y, img)

    def move(self):
        self.x += 1
        if self.x == constants.screen_width:
            random.shuffle(self.cloud_images)
            self.img = self.cloud_images[random.randint(0, 3)]
            self.x = random.randint(-300, - 100)
            self.y = random.randint(100, 700)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
        self.move()

    @classmethod
    def generate_clouds(cls):
        random.shuffle(cls.cloud_images)
        for i in range(0, 4):
            cloud = cls(
                random.randint(0, 700),
                random.randint(0, 700),
                cls.cloud_images[random.randint(0, 3)]
            )
            cls.clouds_list.append(cloud)

    @classmethod
    def draw_clouds(cls, screen):
        for cloud in cls.clouds_list:
            cloud.draw(screen)


class Tree(GameObject):
    def __init__(self, x, y, img, age):
        GameObject.__init__(self, 'tree', x, y, img)
        self.age = age


class House(GameObject):
    def __init__(self, x, y, img):
        GameObject.__init(self, 'house', x, y, img)
