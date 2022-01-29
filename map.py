import pygame, default_game_settings
from help_functions import tile_row_and_column


class MapTile:
    def __init__(self, tile_type, is_visible):
        self.tile_type = tile_type
        self.is_visible = is_visible


class Map:
    grass = pygame.image.load("./img/grass.jpg")
    rock = pygame.image.load("./img/rock.png")
    tree2 = pygame.image.load("./img/tree2.png")
    house1 = pygame.image.load("./img/house1.png")

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
        sliced_rows = self.map_matrix[self.row_index_of_first_visible_tile:]
        visible_map = [row[self.column_index_of_first_visible_tile:] for row in sliced_rows]
        return visible_map

    def draw_whole_map(self):
        map_width = self.map_columns
        map_elements_number = map_width * self.map_rows

        for tile_number in range(map_elements_number):
            # divmod(a, b)
            # (a // b, a % b)
            tile_column_index, tile_row_index = divmod(tile_number, self.map_columns)

            x = (tile_column_index) * default_game_settings.NODE_SIZE
            y = (tile_row_index) * default_game_settings.NODE_SIZE

            if self.map_matrix[tile_row_index][tile_column_index].is_visible:
                self.whole_map_surface.blit(self.grass, (x, y))

                if self.map_matrix[tile_row_index][tile_column_index].tile_type == 1:
                    self.whole_map_surface.blit(self.rock, (x, y))
                elif self.map_matrix[tile_row_index][tile_column_index].tile_type == 2:
                    self.whole_map_surface.blit(self.tree2, (x, y))
                elif self.map_matrix[tile_row_index][tile_column_index].tile_type == 3:
                    self.whole_map_surface.blit(self.house1, (x, y))
            else:
                map_shadow_tile = (
                    x,
                    y,
                    default_game_settings.NODE_SIZE,
                    default_game_settings.NODE_SIZE,
                )
                pygame.draw.rect(self.whole_map_surface, (0, 0, 0), map_shadow_tile, 1)

    def update_shadow_map_tile(self, tile_row_index, tile_column_index):
        if not self.map_matrix[tile_row_index][tile_column_index].is_visible:
            tile_x_coordinate = tile_column_index * default_game_settings.NODE_SIZE
            tile_y_coordinate = tile_row_index * default_game_settings.NODE_SIZE

            self.whole_map_surface.blit(
                self.grass, (tile_x_coordinate, tile_y_coordinate)
            )

            if self.map_matrix[tile_row_index][tile_column_index].tile_type == 1:
                self.whole_map_surface.blit(
                    self.rock, (tile_x_coordinate, tile_y_coordinate)
                )
            elif self.map_matrix[tile_row_index][tile_column_index].tile_type == 2:
                self.whole_map_surface.blit(
                    self.tree2, (tile_x_coordinate, tile_y_coordinate)
                )
            elif self.map_matrix[tile_row_index][tile_column_index].tile_type == 3:
                self.whole_map_surface.blit(
                    self.house1, (tile_x_coordinate, tile_y_coordinate)
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

        node = tile_row_and_column(pygame.mouse.get_pos())
        rect_x = node[1] * default_game_settings.NODE_SIZE
        rect_y = node[0] * default_game_settings.NODE_SIZE
        yellow_border_node_rect = (
            rect_x,
            rect_y,
            default_game_settings.NODE_SIZE,
            default_game_settings.NODE_SIZE,
        )
        pygame.draw.rect(screen, (255, 255, 0), yellow_border_node_rect, 1)


class MiniMap:
    def __init__(self, map, screen_x_position, screen_y_position):
        self.screen_x_position = screen_x_position
        self.screen_y_position = screen_y_position

    def draw(self, screen, map, character):
        self.mini_x = self.screen_x_position + map.column_index_of_first_visible_tile
        self.mini_y = self.screen_y_position + map.row_index_of_first_visible_tile

        self.character_x = self.screen_x_position + character.actual_node(map)[1]
        self.character_y = self.screen_y_position + character.actual_node(map)[0]

        # whole map area
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            (self.screen_x_position, self.screen_y_position, 100, 100),
        )

        # draw visible screen rect
        visible_screen_rect = (
            self.mini_x,
            self.mini_y,
            default_game_settings.GAME_SCREEN_SIZE[0] / default_game_settings.NODE_SIZE,
            default_game_settings.GAME_SCREEN_SIZE[1] / default_game_settings.NODE_SIZE,
        )

        pygame.draw.rect(screen, (200, 200, 200), visible_screen_rect)
        pygame.draw.circle(screen, (200, 0, 0), (self.character_x, self.character_y), 2)
