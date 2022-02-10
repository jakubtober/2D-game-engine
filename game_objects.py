import pygame
import random
from math import sqrt

import default_game_settings
from apath import astar


from help_functions import (
    global_column_to_local_x_coordinate,
    global_row_to_local_y_coordinate, tile_row_and_column,
)


class GameObject:
    def __init__(self, x_coordinate=None, y_coordinate=None, bitmaps=list):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.bitmaps = bitmaps
        self.fps_counter = 0
        self.bitmap_frame_index = 0

    def actual_row_and_column_index(self, map, x_offset: int = 0, y_offset: int = 0):
        actual_tile_row_index = map.row_index_of_first_visible_tile + (
            (self.y_coordinate // default_game_settings.NODE_SIZE)
        )
        tile_column_index = map.column_index_of_first_visible_tile + (
            (self.x_coordinate // default_game_settings.NODE_SIZE)
        )
        return actual_tile_row_index, tile_column_index

    def _animate_bitmaps(self):
        if self.fps_counter >= 10:
            self.fps_counter = 0

            if self.bitmap_frame_index < (len(self.bitmaps) - 1):
                self.bitmap_frame_index += 1
            else:
                self.bitmap_frame_index = 0

        self.fps_counter += 1
        return self.bitmap_frame_index

    def draw(self, screen):
        screen.blit(
            self.bitmaps[self.bitmap_frame_index],
            (self.x_coordinate, self.y_coordinate),
        )
        self._animate_bitmaps()

    def update_map_movement_position(self, tile_column_change, tile_row_change):
        self.x_coordinate += default_game_settings.NODE_SIZE * (
            tile_column_change * (-1)
        )
        self.y_coordinate += default_game_settings.NODE_SIZE * (tile_row_change * (-1))


class Character(GameObject):
    def __init__(self, tile_x: int, tile_y: int, map):
        GameObject.__init__(
            self,
            tile_x * default_game_settings.NODE_SIZE,
            tile_y * default_game_settings.NODE_SIZE,
        )
        self.map = map
        self.tile_column = self.x_coordinate // default_game_settings.NODE_SIZE
        self.tile_row = self.y_coordinate // default_game_settings.NODE_SIZE

        self.start_tile = (
            tile_y // default_game_settings.NODE_SIZE,
            tile_x // default_game_settings.NODE_SIZE,
        )
        self.path_end_tile = ()

        self.is_moving = False
        self.path = []
        self.direction = "E"

        self.character_east_bitmaps = [
            pygame.image.load("./img/character_e/character_e1.png"),
            pygame.image.load("./img/character_e/character_e2.png"),
            pygame.image.load("./img/character_e/character_e3.png"),
        ]
        self.character_west_bitmaps = [
            pygame.image.load("./img/character_w/character_w1.png"),
            pygame.image.load("./img/character_w/character_w2.png"),
            pygame.image.load("./img/character_w/character_w3.png"),
        ]
        self.bitmaps = self.character_east_bitmaps

    def delete_map_shadow_tiles_around(self):
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
                    self.map.delete_shadow_map_tile(
                        tile_row_to_update,
                        tile_column_to_update,
                    )

    def draw(self, screen):
        if self.is_moving:
            if self.direction == "E":
                screen.blit(
                    self.character_east_bitmaps[self.bitmap_frame_index],
                    (self.x_coordinate, self.y_coordinate),
                )
            elif self.direction == "W":
                screen.blit(
                    self.character_west_bitmaps[self.bitmap_frame_index],
                    (self.x_coordinate, self.y_coordinate),
                )

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
            self._animate_bitmaps()
        else:
            if self.direction == "E":
                screen.blit(
                    self.character_east_bitmaps[0],
                    (self.x_coordinate, self.y_coordinate),
                )
            elif self.direction == "W":
                screen.blit(
                    self.character_west_bitmaps[0],
                    (self.x_coordinate, self.y_coordinate),
                )

    def move(self):
        end_tile_x_is_self_x = (
            global_column_to_local_x_coordinate(self.map, self.path_end_tile[1])
            == self.x_coordinate
        )
        end_tile_y_is_self_y = (
            global_row_to_local_y_coordinate(self.map, self.path_end_tile[0])
            == self.y_coordinate
        )
        second_path_tile_x_is_self_x = (
            global_column_to_local_x_coordinate(self.map, self.path[1][1])
            == self.x_coordinate
        )
        second_path_tile_y_is_self_y = (
            global_row_to_local_y_coordinate(self.map, self.path[1][0])
            == self.y_coordinate
        )

        if self.is_moving:
            if end_tile_x_is_self_x and end_tile_y_is_self_y:
                self.is_moving = False
            else:
                if second_path_tile_x_is_self_x and second_path_tile_y_is_self_y:
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
        for tile in path:
            if path.index(tile) < (len(path) - 1):
                next_tile = path[path.index(tile) + 1]
                pygame.draw.line(
                    screen,
                    (255, 255, 0),
                    (
                        (tile[1] * default_game_settings.NODE_SIZE) + 40,
                        (tile[0] * default_game_settings.NODE_SIZE) + 40,
                    ),
                    (
                        (next_tile[1] * default_game_settings.NODE_SIZE) + 40,
                        (next_tile[0] * default_game_settings.NODE_SIZE) + 40,
                    ),
                    3,
                )

    @staticmethod
    def find_path(map, start_tile, end_tile):
        start_tile_not_obstacle = map.map_matrix[start_tile[0]][
            start_tile[1]
        ].is_possible_to_cross
        end_tile_not_obstacle = map.map_matrix[end_tile[0]][
            end_tile[1]
        ].is_possible_to_cross

        if start_tile_not_obstacle and end_tile_not_obstacle:
            path = astar(map.map_matrix, start_tile, end_tile)
            if path:
                return path


class Bird1(GameObject):
    def __init__(self, tile_x: int, tile_y: int, map):
        GameObject.__init__(
            self,
            tile_x * default_game_settings.NODE_SIZE,
            tile_y * default_game_settings.NODE_SIZE,
        )
        self.map = map

        self.is_moving = True
        self.direction = "E"
        self.last_tile_i_waited = (-1, -1)

        self.east_bitmaps = [
            pygame.image.load("./img/bird1_e/bird1_e1.png"),
            pygame.image.load("./img/bird1_e/bird1_e2.png"),
            pygame.image.load("./img/bird1_e/bird1_e3.png"),
        ]
        self.west_bitmaps = [
            pygame.image.load("./img/bird1_w/bird1_w1.png"),
            pygame.image.load("./img/bird1_w/bird1_w2.png"),
            pygame.image.load("./img/bird1_w/bird1_w3.png"),
        ]
        self.bitmaps = self.east_bitmaps

    def _wait_and_turn_direction(self):
        directions = ["E", "W", "S", "N"]
        directions.remove(self.direction)
        self.direction = random.choice(directions)

        if self.fps_counter >= 60:
            self.fps_counter = 0
            self.last_tile_i_waited = self.actual_row_and_column_index(self.map)
            self.is_moving = True

        self.fps_counter += 1

    def move(self):
        if self.is_moving:
            if self.direction == "E":
                self.x_coordinate += 1
            elif self.direction == "W":
                self.x_coordinate -= 1
            elif self.direction == "S":
                self.y_coordinate += 1
            elif self.direction == "N":
                self.y_coordinate -= 1

        if self.actual_row_and_column_index(self.map)[1] < 0:
            self.direction = "E"
        elif self.actual_row_and_column_index(self.map)[1] > 100:
            self.direction = "W"
        elif self.actual_row_and_column_index(self.map)[0] < 0:
            self.direction = "S"
        elif self.actual_row_and_column_index(self.map)[0] > 100:
            self.direction = "N"

    def draw_bitmaps_for_the_right_direction(self, screen):
        if self.direction == "E":
            screen.blit(self.east_bitmaps[self.bitmap_frame_index], (self.x_coordinate, self.y_coordinate))
        elif self.direction == "W":
            screen.blit(self.west_bitmaps[self.bitmap_frame_index], (self.x_coordinate, self.y_coordinate))
        elif self.direction == "S":
            screen.blit(self.west_bitmaps[self.bitmap_frame_index], (self.x_coordinate, self.y_coordinate))
        elif self.direction == "N":
            screen.blit(self.west_bitmaps[self.bitmap_frame_index], (self.x_coordinate, self.y_coordinate))

    def draw(self, screen):
        actual_tile = self.actual_row_and_column_index(
            self.map,
        )
        tile_x_coordinate = global_column_to_local_x_coordinate(
            self.map,
            actual_tile[1],
        )
        tile_y_coordinate = global_row_to_local_y_coordinate(
            self.map,
            actual_tile[0],
        )

        bird_is_on_the_tile = all([
            tile_x_coordinate == self.x_coordinate,
            tile_y_coordinate == self.y_coordinate,
        ])

        is_grass = isinstance(self.map.map_matrix[actual_tile[0]][actual_tile[1]].fixed_tile_game_object, Grass)

        if self.map.map_matrix[actual_tile[0]][actual_tile[1]].is_visible:
            if not bird_is_on_the_tile:
                self.draw_bitmaps_for_the_right_direction(screen)
                self._animate_bitmaps()
                self.move()
            elif bird_is_on_the_tile:
                if is_grass:
                    self.draw_bitmaps_for_the_right_direction(screen)
                    self._animate_bitmaps()
                    self.move()
                elif not is_grass:
                    if self.last_tile_i_waited != actual_tile:
                        self.is_moving = False
                        screen.blit(self.east_bitmaps[0], (self.x_coordinate, self.y_coordinate))
                        self._wait_and_turn_direction()
                    else:
                        self.draw_bitmaps_for_the_right_direction(screen)
                        self._animate_bitmaps()
                        self.move()
        else:
            pass


class Cloud(GameObject):
    cloud_bitmaps = [
        pygame.image.load("./img/cloud1.png"),
        pygame.image.load("./img/cloud2.png"),
        pygame.image.load("./img/cloud3.png"),
        pygame.image.load("./img/cloud4.png"),
    ]

    def __init__(self, x_coordinate, y_coordinate, bitmaps):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmaps)

    def move(self):
        self.x_coordinate += 1
        if self.x_coordinate == default_game_settings.GAME_SCREEN_SIZE[0]:
            random.shuffle(self.cloud_bitmaps)
            self.bitmaps = [self.cloud_bitmaps[random.randint(0, 3)]]
            self.x_coordinate = random.randint(-300, -100)
            self.y_coordinate = random.randint(100, 700)

    def draw(self, screen):
        screen.blit(self.bitmaps[0], (self.x_coordinate, self.y_coordinate))
        self.move()


class Grass(GameObject):
    def __init__(
        self,
        x_coordinate=None,
        y_coordinate=None,
        bitmaps=None,
    ):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmaps)
        if bitmaps is None:
            self.bitmaps = [pygame.image.load("./img/grass.jpg")]


class Tree(GameObject):
    def __init__(
        self,
        x_coordinate=None,
        y_coordinate=None,
        bitmaps=None,
    ):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmaps)
        if bitmaps is None:
            self.bitmaps = [pygame.image.load("./img/tree3.png")]


class PineTree(GameObject):
    def __init__(
        self,
        x_coordinate=None,
        y_coordinate=None,
        bitmaps=None,
    ):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmaps)
        if bitmaps is None:
            self.bitmaps = [pygame.image.load("./img/tree2.png")]


class OldTree(GameObject):
    def __init__(
        self,
        x_coordinate=None,
        y_coordinate=None,
        bitmaps=None,
    ):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmaps)
        if bitmaps is None:
            self.bitmaps = [pygame.image.load("./img/tree4.png")]


class PieceOfWood(GameObject):
    def __init__(
        self,
        x_coordinate=None,
        y_coordinate=None,
        bitmaps=None,
    ):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmaps)
        if bitmaps is None:
            self.bitmaps = [pygame.image.load("./img/piece_of_wood.png")]


class Bushes1(GameObject):
    def __init__(
        self,
        x_coordinate=None,
        y_coordinate=None,
        bitmaps=None,
    ):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmaps)
        if bitmaps is None:
            self.bitmaps = [pygame.image.load("./img/bushes1.png")]


class Rock(GameObject):
    def __init__(
        self,
        x_coordinate=None,
        y_coordinate=None,
        bitmaps=None,
    ):
        GameObject.__init__(self, x_coordinate, y_coordinate, bitmaps)
        if bitmaps is None:
            self.bitmaps = [pygame.image.load("./img/rock.png")]
