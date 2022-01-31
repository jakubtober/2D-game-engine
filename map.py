import pygame, default_game_settings

from game_objects import Character
from help_functions import tile_row_and_column


class MapTile:
    def __init__(self, tile_type, is_visible):
        self.tile_type = tile_type
        self.is_visible = is_visible
        self.bitmap = {
            "grass": pygame.image.load("./img/grass.jpg"),
            "rock": pygame.image.load("./img/rock.png"),
            "tree": pygame.image.load("./img/tree2.png"),
            "house": pygame.image.load("./img/house1.png"),
        }


class Map:
    def __init__(
        self,
        map_matrix: list,
        row_index_of_first_visible_tile: int,
        column_index_of_first_visible_tile: int,
    ):
        self.map_matrix = map_matrix
        self.map_rows = len(map_matrix)
        self.map_columns = len(map_matrix[0])
        self.column_index_of_first_visible_tile = column_index_of_first_visible_tile
        self.row_index_of_first_visible_tile = row_index_of_first_visible_tile

        surface_size = (
            self.map_columns * default_game_settings.NODE_SIZE,
            self.map_rows * default_game_settings.NODE_SIZE,
        )
        self.whole_map_surface = pygame.Surface(surface_size)

    @property
    def visible_map(self):
        sliced_rows = self.map_matrix[self.row_index_of_first_visible_tile :]
        visible_map = [
            row[self.column_index_of_first_visible_tile :] for row in sliced_rows
        ]
        return visible_map

    def draw_whole_map(self):
        map_width = self.map_columns
        map_elements_number = map_width * self.map_rows

        for tile_number in range(map_elements_number):
            # divmod(a, b)
            # (a // b, a % b)
            tile_column_index, tile_row_index = divmod(tile_number, self.map_columns)

            x = tile_column_index * default_game_settings.NODE_SIZE
            y = tile_row_index * default_game_settings.NODE_SIZE

            actual_tile = self.map_matrix[tile_row_index][tile_column_index]

            if actual_tile.is_visible:
                self.whole_map_surface.blit(actual_tile.bitmap["grass"], (x, y))

                if actual_tile.tile_type == "rock":
                    self.whole_map_surface.blit(
                        actual_tile.bitmap[actual_tile.tile_type], (x, y)
                    )
                elif actual_tile.tile_type == "tree":
                    self.whole_map_surface.blit(
                        actual_tile.bitmap[actual_tile.tile_type], (x, y)
                    )
                elif actual_tile.tile_type == "house":
                    self.whole_map_surface.blit(
                        actual_tile.bitmap[actual_tile.tile_type], (x, y)
                    )
            else:
                map_shadow_tile = (
                    x,
                    y,
                    default_game_settings.NODE_SIZE,
                    default_game_settings.NODE_SIZE,
                )
                pygame.draw.rect(self.whole_map_surface, (0, 0, 0), map_shadow_tile, 1)

    def update_shadow_map_tile(self, tile_row_index: int, tile_column_index: int):
        actual_tile = self.map_matrix[tile_row_index][tile_column_index]

        if not actual_tile.is_visible:
            tile_x_coordinate = tile_column_index * default_game_settings.NODE_SIZE
            tile_y_coordinate = tile_row_index * default_game_settings.NODE_SIZE

            self.whole_map_surface.blit(
                actual_tile.bitmap["grass"], (tile_x_coordinate, tile_y_coordinate)
            )

            if actual_tile.tile_type == "rock":
                self.whole_map_surface.blit(
                    actual_tile.bitmap[actual_tile.tile_type],
                    (tile_x_coordinate, tile_y_coordinate),
                )
            elif actual_tile.tile_type == "tree":
                self.whole_map_surface.blit(
                    actual_tile.bitmap[actual_tile.tile_type],
                    (tile_x_coordinate, tile_y_coordinate),
                )
            elif actual_tile.tile_type == "house":
                self.whole_map_surface.blit(
                    actual_tile.bitmap[actual_tile.tile_type],
                    (tile_x_coordinate, tile_y_coordinate),
                )

    def display_visible_map_surface(self, screen):
        visible_map_rect = (
            self.column_index_of_first_visible_tile * default_game_settings.NODE_SIZE,
            self.row_index_of_first_visible_tile * default_game_settings.NODE_SIZE,
            default_game_settings.GAME_SCREEN_SIZE[0],
            default_game_settings.GAME_SCREEN_SIZE[1],
        )
        screen.blit(self.whole_map_surface, (0, 0), visible_map_rect)

        # draw yellow border around node that is pointed by the mouse

        tile = tile_row_and_column(pygame.mouse.get_pos())
        rect_x_coordinate = tile[1] * default_game_settings.NODE_SIZE
        rect_y_coordinate = tile[0] * default_game_settings.NODE_SIZE
        yellow_border_node_rect = (
            rect_x_coordinate,
            rect_y_coordinate,
            default_game_settings.NODE_SIZE,
            default_game_settings.NODE_SIZE,
        )
        pygame.draw.rect(screen, (255, 255, 0), yellow_border_node_rect, 1)


class MiniMap:
    def __init__(
        self, visible_screen_x_coordinate: int, visible_screen_y_coordinate: int
    ):
        self.visible_screen_x_coordinate = visible_screen_x_coordinate
        self.visible_screen_y_coordinate = visible_screen_y_coordinate

    def draw(self, screen, map: Map, character: Character):
        mini_x_coordinate_on_visible_screen = (
            self.visible_screen_x_coordinate + map.column_index_of_first_visible_tile
        )
        mini_y_coordinate_on_visible_screen = (
            self.visible_screen_y_coordinate + map.row_index_of_first_visible_tile
        )

        mini_map_character_x_coordinate = (
            self.visible_screen_x_coordinate
            + character.actual_row_and_column_index(map)[1]
        )
        mini_map_character_y_coordinate = (
            self.visible_screen_y_coordinate
            + character.actual_row_and_column_index(map)[0]
        )

        # whole map area
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            (
                self.visible_screen_x_coordinate,
                self.visible_screen_y_coordinate,
                100,
                100,
            ),
        )

        # draw visible screen rect
        visible_screen_rect = (
            mini_x_coordinate_on_visible_screen,
            mini_y_coordinate_on_visible_screen,
            default_game_settings.GAME_SCREEN_SIZE[0] / default_game_settings.NODE_SIZE,
            default_game_settings.GAME_SCREEN_SIZE[1] / default_game_settings.NODE_SIZE,
        )

        pygame.draw.rect(screen, (200, 200, 200), visible_screen_rect)
        pygame.draw.circle(
            screen,
            (200, 0, 0),
            (mini_map_character_x_coordinate, mini_map_character_y_coordinate),
            2,
        )
