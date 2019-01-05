import sys, pygame, time, random
from pygame.locals import *
from apath import astar
from help_functions import node_info
from apath import MAP_OBSTACLES

class GameObject():
    objects_list = []

    def __init__(self, object_type, x, y, img=None):
        self.object_type = object_type
        self.objects_list.append(self)
        self.x = x
        self.y = y
        self.img = img

    def actual_node(self, map):
        actual_node_column = map.first_node_column + (self.x // 80)
        actual_node_row = map.first_node_row + (self.y // 80)
        return (actual_node_row, actual_node_column)

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.x, self.y))


class Character(GameObject):
    def __init__(self, object_type, node_x, node_y):
        GameObject.__init__(self, 'knight', node_x * 80, node_y * 80)
        self.node_column = self.x // 80
        self.node_row = self.y // 80

        self.start_node = (node_y // 80, node_x // 80)
        self.end_node = ()

        self.is_moving = False
        self.path = []
        self.direction = 'E'

        if self.object_type == 'knight':
            self.character_east = pygame.image.load('./img/knight_east.png')
            self.character_west = pygame.image.load('./img/knight_west.png')

    @property
    def visible_map_node(self):
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
                        self.path[1] = self.visible_map_node
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
        if self.x == 800:
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
