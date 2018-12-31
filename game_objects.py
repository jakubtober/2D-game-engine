import sys, pygame, time, random
from pygame.locals import *
from apath import astar
from help_functions import node_info
from apath import MAP_OBSTACLES

class GameObject():
    def __init__(self, object_type, x, y, img=None):
        self.object_type = object_type
        self.x = x
        self.y = y
        self.img = img

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.x, self.y))


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


    def draw(self, screen):
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


class Character(GameObject):
    def __init__(self, object_type, node_x, node_y):
        GameObject.__init__(self, 'knight', node_x * 80, node_y * 80)
        self.node_column = self.x // 80
        self.node_row = self.y // 80
        self.is_moving = False
        self.start_node = (node_y // 80, node_x // 80)
        self.end_node = ()
        self.path = []
        self.direction = 'E'

        if self.object_type == 'knight':
            self.character_east = pygame.image.load('./img/knight_east.png')
            self.character_west = pygame.image.load('./img/knight_west.png')

    @property
    def node(self):
        return (self.y // 80, self.x // 80)

    def draw(self, screen):
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

    def draw_path(self, screen, path):
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

    def find_and_draw_path(self, screen, test_map, start_node, end_node):
        start_node_not_obsticle = (test_map[start_node[0]][start_node[1]] not in MAP_OBSTACLES)
        end_node_not_obsticle = (test_map[end_node[0]][end_node[1]] not in MAP_OBSTACLES)

        if start_node_not_obsticle and end_node_not_obsticle:
            path = astar(test_map, start_node, end_node)
            if path:
                self.draw_path(screen, path)
                return path

    def update_map_movement_position(self, node_column_change, node_row_change):
        self.x += 80 * (node_column_change * (-1))
        self.y += 80 * (node_row_change * (-1))
        self.start_node = (
            self.start_node[0] + (node_row_change * (-1)),
            self.start_node[1] + (node_column_change * (-1)),
        )
        if self.is_moving:
            self.end_node = (
                self.end_node[0] + (node_row_change * (-1)),
                self.end_node[1] + (node_column_change * (-1)),
            )
            self.path = [(node[0] + (node_row_change * (-1)), node[1] + (node_column_change * (-1))) for node in self.path]


class Cloud(GameObject):
    def __init__(self, object_type, x, y, img):
        GameObject.__init__(self, 'cloud', x, y, img)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
        self.x += 1
        if self.x == 800:
            self.x = -100
            self.y = random.randint(100, 700)
