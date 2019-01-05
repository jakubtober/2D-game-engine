import pygame
import random
from help_functions import node_info

class Map():
    grass = pygame.image.load("./img/grass.jpg")
    rock = pygame.image.load("./img/rock.png")
    tree2 = pygame.image.load("./img/tree2.png")
    house1 = pygame.image.load("./img/house1.png")

    def __init__(self, map, first_node_row, first_node_column):
        self.first_node_column = first_node_column
        self.first_node_row = first_node_row
        self.map = map
        self.whole_map_surface = pygame.Surface((80*100, 80*100))

    @property
    def visible_map(self):
        sliced_rows = self.map[self.first_node_row:]
        visible_map = [row[self.first_node_column:] for row in sliced_rows]
        return visible_map

    def draw_whole_map(self):
        visible_map_width = 100
        map_elements_number = visible_map_width * 100

        for node_number in range(map_elements_number):
            # divmod(a, b)
            # (a // b, a % b)
            node_column, node_row = divmod(node_number, 100)

            x = (node_column) * 80
            y = (node_row) * 80

            self.whole_map_surface.blit(self.grass, (x, y))

            if self.map[node_row][node_column] == 1:
                self.whole_map_surface.blit(self.rock, (x, y))
            elif self.map[node_row][node_column] == 2:
                self.whole_map_surface.blit(self.tree2, (x, y))
            elif self.map[node_row][node_column] == 3:
                self.whole_map_surface.blit(self.house1, (x, y))

    def display_whole_map_surface(self, screen):
        screen.blit(self.whole_map_surface,
            (0, 0),
            (self.first_node_column*80, self.first_node_row*80, 800, 800)
        )

        # draw yellow border around node that is pointed by the mouse
        node = node_info(pygame.mouse.get_pos())
        rect_x = node[1] * 80
        rect_y = node[0] * 80
        pygame.draw.rect(screen, (255, 255, 0), (rect_x, rect_y, 80, 80), 1)


class MiniMap():
    def __init__(self, map, screen_x_position, screen_y_position):
        self.screen_x_position = screen_x_position
        self.screen_y_position = screen_y_position

    def draw(self, screen, map, character):
        self.mini_x = self.screen_x_position + map.first_node_column
        self.mini_y = self.screen_y_position + map.first_node_row

        self.character_x = self.screen_x_position + character.actual_node(map)[1]
        self.character_y = self.screen_y_position + character.actual_node(map)[0]

        pygame.draw.rect(
            screen,
            (100, 100, 100),
            (self.screen_x_position, self.screen_y_position, 100, 100)
        )
        pygame.draw.rect(screen, (200, 200, 200), (self.mini_x, self.mini_y, 8, 8))
        pygame.draw.circle(
            screen,
            (200, 0, 0),
            (self.character_x, self.character_y),
            2
        )
