import pygame
import os
from enum import Enum
from numpy.random import choice

# standard paddle consisting of 12 rectangles with corresponding angle; order left to right
STD_SIZE_PADDLE = [[pygame.Rect(300, 509, 5, 3), 120],
                   [pygame.Rect(305, 506, 5, 6), 120],
                   [pygame.Rect(310, 503, 5, 9), 120],
                   [pygame.Rect(315, 500, 10, 12), 80],
                   [pygame.Rect(325, 500, 10, 12), 80],
                   [pygame.Rect(335, 500, 10, 12), 80],
                   [pygame.Rect(345, 500, 10, 12), 100],
                   [pygame.Rect(355, 500, 10, 12), 100],
                   [pygame.Rect(365, 500, 10, 12), 100],
                   [pygame.Rect(375, 503, 5, 9), 45],
                   [pygame.Rect(380, 506, 5, 6), 45],
                   [pygame.Rect(385, 509, 5, 3), 45]
                   ]

STD_PADDLE_SPEED = 5

STD_FORM_BALL = pygame.Rect(300, 490, 5, 5)

BRICK_WIDTH = 25
BRICK_HEIGHT = 10
COLOR_UNBREAKABLE_BRICK = (135, 135, 135)

CRNT_PATH = os.path.dirname(__file__)   # Where your .py file is located
BSI_path = os.path.join(CRNT_PATH, 'brick_state_images')    # The Brick State Images folder path

SPECIAL_WIDTH = 25
SPECIAL_HEIGHT = 10

class Paddle:
    def __init__(self):
        self.hitzones = STD_SIZE_PADDLE
        self.triangle_views = self.create_triangles()
        self.speed = STD_PADDLE_SPEED

    def add_special(self, special):
        self.special = special

    def tick(self):
        self.special.time = self.special.time - 1

    def change_size(self):
        pass

    def reset_size(self):
        self.hitzones = STD_SIZE_PADDLE

    """
        description
            - changes the paddle's part's x-coordinates to change its position on the screen using self.speed
        :param direction: 1 for right-movement, -1 for left-movement
    """
    def move(self, direction):
        for paddle_part in self.hitzones:
            paddle_part[0].x += self.speed * direction
        self.triangle_views = self.create_triangles()

    def update_triangles(self):
        self.triangle_views = self.create_triangles()

    def create_triangles(self):
        return ([self.hitzones[0][0].topleft,
                 self.hitzones[3][0].topleft,
                (self.hitzones[3][0].x, self.hitzones[0][0].y)],
                [self.hitzones[11][0].topright,
                 self.hitzones[8][0].topright,
                (self.hitzones[8][0].x + self.hitzones[8][0].width, self.hitzones[11][0].y)])


class Ball:
    def __init__(self):
        self.form = STD_FORM_BALL

    def add_special(self, special):
        self.special = special

    def tick(self):
        self.special.time = self.special.time - 1

    def move(self):
        pass


class Brick:

    brick_state_images = [pygame.image.load(os.path.join(BSI_path,'brick_state_0.png')),
                          pygame.image.load(os.path.join(BSI_path,'brick_state_1.png')),
                          pygame.image.load(os.path.join(BSI_path,'brick_state_2.png')),
                          pygame.image.load(os.path.join(BSI_path,'brick_state_3.png')),
                          pygame.image.load(os.path.join(BSI_path,'brick_state_4.png')),
                          pygame.image.load(os.path.join(BSI_path,'brick_state_5.png'))]

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
    c = choice([False, True], 1, [0.01, 0.99]) # Hier WSLKT Anpassen falls zu viele / wenige Powerups kommen
    return c[0]