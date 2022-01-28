import pygame, random, constants
from help_functions import node_info


class MapTile():
    def __init__(self, tile_type, is_visible):
        self.tile_type = tile_type
        self.is_visible = is_visible


class Map():
    grass = pygame.image.load("./img/grass.jpg")
    rock = pygame.image.load("./img/rock.png")
    tree2 = pygame.image.load("./img/tree2.png")
    house1 = pygame.image.load("./img/house1.png")

    def __init__(self, map, first_node_row, first_node_column):
        self.map = map
        self.map_rows = len(map)
        self.map_columns = len(map[0])
        self.first_node_column = first_node_column
        self.first_node_row = first_node_row

        surface_size = (
            self.map_columns*constants.NODE_SIZE,
            self.map_rows*constants.NODE_SIZE
        )
        self.whole_map_surface = pygame.Surface(surface_size)

    @property
    def visible_map(self):
        sliced_rows = self.map[self.first_node_row:]
        visible_map = [row[self.first_node_column:] for row in sliced_rows]
        return visible_map

    def draw_whole_map(self):
        map_width = self.map_columns
        map_elements_number = map_width * self.map_rows

        for node_number in range(map_elements_number):
            # divmod(a, b)
            # (a // b, a % b)
            node_column, node_row = divmod(node_number, self.map_columns)

            x = (node_column) * constants.NODE_SIZE
            y = (node_row) * constants.NODE_SIZE

            if self.map[node_row][node_column].is_visible:
                self.whole_map_surface.blit(self.grass, (x, y))

                if self.map[node_row][node_column].tile_type == 1:
                    self.whole_map_surface.blit(self.rock, (x, y))
                elif self.map[node_row][node_column].tile_type == 2:
                    self.whole_map_surface.blit(self.tree2, (x, y))
                elif self.map[node_row][node_column].tile_type == 3:
                    self.whole_map_surface.blit(self.house1, (x, y))
            else:
                map_shadow_tile = (
                    x,
                    y,
                    constants.NODE_SIZE,
                    constants.NODE_SIZE
                )
                pygame.draw.rect(self.whole_map_surface, (0, 0, 0), map_shadow_tile, 1)

    def update_shadow_map_tile(self, tile_row, tile_column):
        if not self.map[tile_row][tile_column].is_visible:
            tile_x_coordinate = tile_column * constants.NODE_SIZE
            tile_y_coordinate = tile_row * constants.NODE_SIZE

            self.whole_map_surface.blit(self.grass, (tile_x_coordinate, tile_y_coordinate))

            if self.map[tile_row][tile_column].tile_type == 1:
                self.whole_map_surface.blit(self.rock, (tile_x_coordinate, tile_y_coordinate))
            elif self.map[tile_row][tile_column].tile_type == 2:
                self.whole_map_surface.blit(self.tree2, (tile_x_coordinate, tile_y_coordinate))
            elif self.map[tile_row][tile_column].tile_type == 3:
                self.whole_map_surface.blit(self.house1, (tile_x_coordinate, tile_y_coordinate))

    def display_visible_map_surface(self, screen):
        visible_map_rect = (
            self.first_node_column*constants.NODE_SIZE,
            self.first_node_row*constants.NODE_SIZE,
            constants.screen_width,
            constants.screen_height
        )
        screen.blit(self.whole_map_surface, (0, 0), visible_map_rect)

        # draw yellow border around node that is pointed by the mouse

        node = node_info(pygame.mouse.get_pos())
        rect_x = node[1] * constants.NODE_SIZE
        rect_y = node[0] * constants.NODE_SIZE
        yellow_border_node_rect = (
            rect_x,
            rect_y,
            constants.NODE_SIZE,
            constants.NODE_SIZE
        )
        pygame.draw.rect(screen, (255, 255, 0), yellow_border_node_rect, 1)


class MiniMap():
    def __init__(self, map, screen_x_position, screen_y_position):
        self.screen_x_position = screen_x_position
        self.screen_y_position = screen_y_position

    def draw(self, screen, map, character):
        self.mini_x = self.screen_x_position + map.first_node_column
        self.mini_y = self.screen_y_position + map.first_node_row

        self.character_x = self.screen_x_position + character.actual_node(map)[1]
        self.character_y = self.screen_y_position + character.actual_node(map)[0]

        # whole map area
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            (self.screen_x_position, self.screen_y_position, 100, 100)
        )

        # draw visible screen rect
        visible_screen_rect = (
            self.mini_x,
            self.mini_y,
            constants.screen_width / constants.NODE_SIZE,
            constants.screen_height / constants.NODE_SIZE
        )

        pygame.draw.rect(screen, (200, 200, 200), visible_screen_rect)
        pygame.draw.circle(
            screen,
            (200, 0, 0),
            (self.character_x, self.character_y),
            2
        )
