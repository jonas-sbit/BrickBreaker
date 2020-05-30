import pygame
import os
from enum import Enum
from numpy.random import choice


DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# standard paddle consisting of 10 rectangles with corresponding bounce-off vector; order left to right
"""STD_SIZE_PADDLE = [[pygame.Rect(300, 508, 8, 4), (-5, -1)],
                   [pygame.Rect(308, 504, 8, 8), (-4, -2)],
                   [pygame.Rect(316, 500, 10, 12), (-3, -3)],
                   [pygame.Rect(326, 500, 10, 12), (-2, -4)],
                   [pygame.Rect(336, 500, 10, 12), (-1, -5)],
                   [pygame.Rect(346, 500, 10, 12), (1, -5)],
                   [pygame.Rect(356, 500, 10, 12), (2, -4)],
                   [pygame.Rect(366, 500, 10, 12), (3, -3)],
                   [pygame.Rect(376, 504, 8, 8), (4, -2)],
                   [pygame.Rect(384, 508, 8, 4), (5, -1)]
                   ]"""

# standard paddle consisting of 12 rectangles with corresponding bounce-off vector; order left to right
# each rect 8 wide and speed =
STD_SIZE_PADDLE = [[pygame.Rect(320, 508, 8, 4), (-5, -1)],
                   [pygame.Rect(328, 504, 8, 8), (-4, -2)],
                   [pygame.Rect(336, 500, 8, 12), (-3, -3)],
                   [pygame.Rect(344, 500, 8, 12), (-2, -4)],
                   [pygame.Rect(352, 500, 8, 12), (-2, -4)],
                   [pygame.Rect(360, 500, 8, 12), (-1, -5)],
                   [pygame.Rect(368, 500, 8, 12), (1, -5)],
                   [pygame.Rect(376, 500, 8, 12), (2, -4)],
                   [pygame.Rect(384, 500, 8, 12), (2, -4)],
                   [pygame.Rect(392, 500, 8, 12), (3, -3)],
                   [pygame.Rect(400, 504, 8, 8), (4, -2)],
                   [pygame.Rect(408, 508, 8, 4), (5, -1)]
                   ]

STD_PADDLE_SPEED = 8

STD_FORM_BALL = pygame.Rect(315, 490, 5, 5)

BRICK_WIDTH = 25
BRICK_HEIGHT = 10
COLOR_UNBREAKABLE_BRICK = (135, 135, 135)

CRNT_PATH = os.path.dirname(__file__)  # Where your .py file is located
BSI_path = os.path.join(CRNT_PATH, 'brick_state_images')  # The Brick State Images folder path

SPECIAL_WIDTH = 25
SPECIAL_HEIGHT = 10


class Movement(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Paddle:
    def __init__(self):
        self.hitzones = STD_SIZE_PADDLE.copy()
        self.triangle_views = self.create_triangles()
        self.speed = STD_PADDLE_SPEED
        self.special = None

    def add_special(self, special):
        self.special = special

    def tick(self):
        self.special.time = self.special.time - 1

    def change_size(self):
        pass

    def reset_size(self):
        # TODO: update coordinates
        self.hitzones = STD_SIZE_PADDLE.copy()

    def move(self, direction):
        """
        description
            - changes the paddle's part's x-coordinates to change its position on the screen using self.speed
        :param direction: 1 for right-movement, -1 for left-movement
        :return: nothing
        """
        over_edge = True
        if not over_edge:
            if not (self.hitzones[0][0].left + (self.speed * direction)) > DISPLAY_WIDTH and \
                    not (self.hitzones[len(self.hitzones)-1][0].right + (self.speed * direction)) < 0:
                for paddle_part in self.hitzones:
                    paddle_part[0].x += self.speed * direction
                self.triangle_views = self.create_triangles()
        else:
            for paddle_part in self.hitzones:
                paddle_part[0].x += self.speed * direction
                if direction == 1:                                  # right movement
                    if paddle_part[0].left >= DISPLAY_WIDTH:
                        paddle_part[0].x = 0
                else:
                    if paddle_part[0].right <= 0:
                        paddle_part[0].x = DISPLAY_WIDTH - paddle_part[0].width
        self.triangle_views = self.create_triangles()

    def update_triangles(self):
        """
        description:
            - Update self.triangles_views to the current paddle position by calling self.create_triangles.
        :return: nothing
        """
        self.triangle_views = self.create_triangles()

    def create_triangles(self):
        """
        description:
            - Calculate the tuples / coordinates to draw the triangles (polygons) visually covering up the rectangles
              used to build the declining part of the paddle
        :return: tuple of two lists containing the tuples / coordinates
        """
        """return ([self.hitzones[0][0].topleft,
                 self.hitzones[2][0].topleft,
                 (self.hitzones[2][0].left, self.hitzones[0][0].y)],
                [self.hitzones[len(self.hitzones) - 1][0].topright,
                 self.hitzones[len(self.hitzones) - 3][0].topright,
                 (self.hitzones[len(self.hitzones) - 3][0].right, self.hitzones[len(self.hitzones) - 1][0].top)])"""
        return ([self.hitzones[0][0].topleft,
                 self.hitzones[0][0].topright,
                (self.hitzones[0][0].right, self.hitzones[1][0].top)],
                [self.hitzones[1][0].topleft,
                 self.hitzones[1][0].topright,
                (self.hitzones[1][0].right, self.hitzones[2][0].top)],
                [self.hitzones[len(self.hitzones) - 1][0].topright,
                 self.hitzones[len(self.hitzones) - 1][0].topleft,
                (self.hitzones[len(self.hitzones) - 1][0].left, self.hitzones[len(self.hitzones) - 2][0].top)],
                [self.hitzones[len(self.hitzones) - 2][0].topright,
                 self.hitzones[len(self.hitzones) - 2][0].topleft,
                (self.hitzones[len(self.hitzones) - 2][0].left, self.hitzones[len(self.hitzones) - 3][0].top)])


class Ball:
    def __init__(self, vector: tuple):
        self.form = STD_FORM_BALL
        self.vector = vector

    def add_special(self, special):
        self.special = special

    def tick(self):
        self.special.time = self.special.time - 1

    def get_horizontal_movement(self):
        """

        :return:
        """
        if self.vector[0] > 0:
            return Movement.RIGHT
        else:
            return Movement.LEFT

    def get_vertical_movement(self):
        """

        :return:
        """
        if self.vector[1] > 0:
            return Movement.DOWN
        else:
            return Movement.UP

    def move(self):
        self.form.x += self.vector[0]
        self.form.y += self.vector[1]

    def get_previous_position(self):
        return self.form.x - self.vector[0], self.form.y - self.vector[1]

    def collide_horizontal(self):
        self.vector = (self.vector[0], self.vector[1] * -1)

    def collide_vertical(self):
        self.vector = (self.vector[0] * -1, self.vector[1])


class Brick:
    brick_state_images = [pygame.image.load(os.path.join(BSI_path, 'brick_state_0.png')),
                          pygame.image.load(os.path.join(BSI_path, 'brick_state_1.png')),
                          pygame.image.load(os.path.join(BSI_path, 'brick_state_2.png')),
                          pygame.image.load(os.path.join(BSI_path, 'brick_state_3.png')),
                          pygame.image.load(os.path.join(BSI_path, 'brick_state_4.png')),
                          pygame.image.load(os.path.join(BSI_path, 'brick_state_5.png'))]

    def __init__(self, coordinates, max_hits):
        """
            description:
                - creates a new object of the brick class
            :param max_hits: number of times the brick has to get hit in order to get destroyed; -1 for unbreakable brick
            :param coordinates: a tuple containing the x- and y-coordinate of the brick's starting point
        """
        self.rect = pygame.Rect(coordinates[0], coordinates[1], BRICK_WIDTH, BRICK_HEIGHT)
        self.hits_left = max_hits

    def get_hit(self):
        """
            description:
                - decrement hits_left if bricks is not unbreakable (i.e. hits_left = -1)
            :return: boolean whether hits_left was decremented to 0
        """
        if self.hits_left > 0:
            self.hits_left -= 1
        return self.hits_left == 0

    def show_brick(self, screen):
        """
            description:
                - select color/background based on self.hits_left
        :return:
        """

        if self.hits_left == -1:
            pygame.draw.rect(screen, COLOR_UNBREAKABLE_BRICK, self.rect)
        else:
            screen.blit(self.brick_state_images[self.hits_left - 1], self.rect)


class Special():

    def __init__(self, start_coordinates):
        """
            description:
                - creates a new object of the special class
            :param start_coordinates: a tuple containing the x- and y-coordinate of the brick's starting point
        """
        self.rect = pygame.Rect(start_coordinates[0], start_coordinates[1], SPECIAL_WIDTH, SPECIAL_HEIGHT)

    def show_special(self):
        """
            description:
                - shows the special, has to be called in a loop  
        """
        self.special_type = Random_Special_Chooser()

    def activate_special(self):
        """
            description:
                - activates the special if its 'catched' 
        """
        if self.special_type == SpecialType.Faster:
            pass
        elif self.special_type == SpecialType.Bigger_Paddle:
            pass
        elif self.special_type == SpecialType.Smaller_Paddle:
            pass
        elif self.special_type == SpecialType.Confused_Controls:
            pass
        elif self.special_type == SpecialType.Extra_Life:
            pass


class SpecialType(Enum):
    Faster = 0
    Slower = 1
    Bigger_Paddle = 2
    Smaller_Paddle = 3
    Confused_Controls = 4
    Extra_Life = 5


def Random_Special_Chooser():
    c = choice([
        SpecialType.Faster,
        SpecialType.Slower,
        SpecialType.Bigger_Paddle,
        SpecialType.Smaller_Paddle,
        SpecialType.Confused_Controls,
        SpecialType.Extra_Life],
        1,
        [
            0.2,
            0.2,
            0.2,
            0.2,
            0.1,
            0.1,
        ]
    )
    return c[0]


def Random_Show_Special():
    c = choice([False, True], 1, [0.01, 0.99])  # Hier WSLKT Anpassen falls zu viele / wenige Powerups kommen
    return c[0]
