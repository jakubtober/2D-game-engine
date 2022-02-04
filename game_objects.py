import pygame
import random
from math import sqrt

import default_game_settings
from apath import astar, MAP_OBSTACLES


from help_functions import (
    global_column_to_local_x_coordinate,
    global_row_to_local_y_coordinate,
)


class GameObject:
    def __init__(self, x_coordinate=None, y_coordinate=None, bitmap=None):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.bitmap = bitmap

    def actual_row_and_column_index(self, map):
        actual_tile_row_index = map.row_index_of_first_visible_tile + (
            self.y_coordinate // default_game_settings.NODE_SIZE
        )
        tile_column_index = map.column_index_of_first_visible_tile + (
            self.x_coordinate // default_game_settings.NODE_SIZE
        )
        return (actual_tile_row_index, tile_column_index)

    def draw(self, screen):
        if self.bitmap:
            screen.blit(self.bitmap, (self.x_coordinate, self.y_coordinate))


class Character(GameObject):
    def __init__(self, node_x: int, node_y: int, map):
        GameObject.__init__(
            self,
            node_x * default_game_settings.NODE_SIZE,
            node_y * default_game_settings.NODE_SIZE,
        )
        self.map = map
        self.node_column = self.x_coordinate // default_game_settings.NODE_SIZE
        self.node_row = self.y_coordinate // default_game_settings.NODE_SIZE

        self.start_node = (
            node_y // default_game_settings.NODE_SIZE,
            node_x // default_game_settings.NODE_SIZE,
        )
        self.path_end_tile = ()

        self.is_moving = False
        self.path = []
        self.direction = "E"

        self.character_east = pygame.image.load("./img/knight_east.png")
        self.character_west = pygame.image.load("./img/knight_west.png")
        self.update_map_shadow_tiles_around()

    def update_map_shadow_tiles_around(self):
        actual_character_tile = self.actual_row_and_column_index(self.map)
        for tile_row_to_update in range(
            actual_character_tile[0] - 3, actual_character_tile[0] + 4
        ):
            for tile_column_to_update in range(
                actual_character_tile[1] - 3, actual_character_tile[1] + 4
            ):
                distance_to_character = sqrt(
                    (tile_row_to_update - actual_character_tile[0]) ** 2
                    + (tile_column_to_update - actual_character_tile[1]) ** 2
                )
                if distance_to_character <= 4:
                    self.map.update_shadow_map_tile(
                        tile_row_to_update,
                        tile_column_to_update,
                    )

    def draw(self, screen):
        if self.direction == "E":
            screen.blit(self.character_east, (self.x_coordinate, self.y_coordinate))
        elif self.direction == "W":
            screen.blit(self.character_west, (self.x_coordinate, self.y_coordinate))

        if self.is_moving:
            circle_x = (
                global_column_to_local_x_coordinate(self.map, (self.path_end_tile[1]))
                + 40
            )
            circle_y = (
                global_row_to_local_y_coordinate(self.map, (self.path_end_tile[0])) + 40
            )

            pygame.draw.circle(
                screen,
                (200, 0, 0),
                (circle_x, circle_y),
                default_game_settings.NODE_SIZE // 4,
                3,
            )

    def move(self):
        end_node_x_is_self_x = (
            global_column_to_local_x_coordinate(self.map, self.path_end_tile[1])
            == self.x_coordinate
        )
        end_node_y_is_self_y = (
            global_row_to_local_y_coordinate(self.map, self.path_end_tile[0])
            == self.y_coordinate
        )
        second_path_node_x_is_self_x = (
            global_column_to_local_x_coordinate(self.map, self.path[1][1])
            == self.x_coordinate
        )
        second_path_node_y_is_self_y = (
            global_row_to_local_y_coordinate(self.map, self.path[1][0])
            == self.y_coordinate
        )

        if self.is_moving:
            if end_node_x_is_self_x and end_node_y_is_self_y:
                self.is_moving = False
            else:
                if second_path_node_x_is_self_x and second_path_node_y_is_self_y:
                    self.path[1] = self.actual_row_and_column_index(self.map)
                    self.path.pop(0)
                else:
                    if (
                        global_column_to_local_x_coordinate(self.map, self.path[1][1])
                        - self.x_coordinate
                    ) < 0:
                        self.x_coordinate -= 1
                        self.direction = "W"
                    elif (
                        global_column_to_local_x_coordinate(self.map, self.path[1][1])
                        - self.x_coordinate
                    ) > 0:
                        self.x_coordinate += 1
                        self.direction = "E"
                    if (
                        global_row_to_local_y_coordinate(self.map, self.path[1][0])
                        - self.y_coordinate
                    ) < 0:
                        self.y_coordinate -= 1
                    elif (
                        global_row_to_local_y_coordinate(self.map, self.path[1][0])
                        - self.y_coordinate
                    ) > 0:
                        self.y_coordinate += 1

    @staticmethod
    def draw_path(screen, path):
        for node in path:
            if path.index(node) < (len(path) - 1):
                next_node = path[path.index(node) + 1]
                pygame.draw.line(
                    screen,
                    (255, 255, 0),
                    (
                        (node[1] * default_game_settings.NODE_SIZE) + 40,
                        (node[0] * default_game_settings.NODE_SIZE) + 40,
                    ),
                    (
                        (next_node[1] * default_game_settings.NODE_SIZE) + 40,
                        (next_node[0] * default_game_settings.NODE_SIZE) + 40,
                    ),
                    3,
                )

    @staticmethod
    def find_path(map, start_node, end_node):
        start_node_not_obstacle = (
            map.map_matrix[start_node[0]][start_node[1]].tile_type not in MAP_OBSTACLES
        )
        end_node_not_obstacle = (
            map.map_matrix[end_node[0]][end_node[1]].tile_type not in MAP_OBSTACLES
        )

        if start_node_not_obstacle and end_node_not_obstacle:
            path = astar(map.map_matrix, start_node, end_node)
            if path:
                return path

    def update_map_movement_position(self, node_column_change, node_row_change):
        self.x_coordinate += default_game_settings.NODE_SIZE * (
            node_column_change * (-1)
        )
        self.y_coordinate += default_game_settings.NODE_SIZE * (node_row_change * (-1))


class Cloud(GameObject):
    clouds_list = []
    cloud_bitmaps = [
        pygame.image.load("./img/cloud1.png"),
        pygame.image.load("./img/cloud2.png"),
        pygame.image.load("./img/cloud3.png"),
        pygame.image.load("./img/cloud4.png"),
    ]

    def __init__(self, x_coordinate, y_coordinate, bitmap):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmap)

    def move(self):
        self.x_coordinate += 1
        if self.x_coordinate == default_game_settings.GAME_SCREEN_SIZE[0]:
            random.shuffle(self.cloud_bitmaps)
            self.bitmap = self.cloud_bitmaps[random.randint(0, 3)]
            self.x_coordinate = random.randint(-300, -100)
            self.y_coordinate = random.randint(100, 700)

    def draw(self, screen):
        screen.blit(self.bitmap, (self.x_coordinate, self.y_coordinate))
        self.move()

    @classmethod
    def generate_clouds(cls):
        random.shuffle(cls.cloud_bitmaps)
        for i in range(0, 4):
            cloud = cls(
                random.randint(0, 700),
                random.randint(0, 700),
                cls.cloud_bitmaps[random.randint(0, 3)],
            )
            cls.clouds_list.append(cloud)

    @classmethod
    def draw_clouds(cls, screen):
        for cloud in cls.clouds_list:
            cloud.draw(screen)


class Grass(GameObject):
    def __init__(
        self,
        x_coordinate=None,
        y_coordinate=None,
        bitmap=pygame.image.load("./img/grass.jpg"),
    ):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmap)


class Tree(GameObject):
    def __init__(
        self,
        x_coordinate=None,
        y_coordinate=None,
        bitmap=pygame.image.load("./img/tree2.png"),
    ):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmap)


class House(GameObject):
    def __init__(
        self,
        x_coordinate=None,
        y_coordinate=None,
        bitmap=pygame.image.load("./img/rock.png"),
    ):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmap)


class Rock(GameObject):
    def __init__(
        self,
        x_coordinate=None,
        y_coordinate=None,
        bitmap=pygame.image.load("./img/house1.png"),
    ):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmap)
