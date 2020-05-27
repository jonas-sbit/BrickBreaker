import pygame

STDRD_SIZE_PADDLE = [[pygame.Rect(300, 500, 20, 10), 120],
                     [pygame.Rect(320, 500, 20, 10), 100],
                     [pygame.Rect(340, 500, 20, 10), 80],
                     [pygame.Rect(360, 500, 20, 10), 45],
                     ]

STNDRD_FORM_BALL = pygame.Rect(300, 490, 5, 5)

BRICK_WIDTH = 25
BRICK_HEIGHT = 10
COLORS_BRICKS = [(255, 153, 153), (255, 0, 0), (153, 0, 0)]
COLOR_UNBREAKABLE_BRICK = ()


class Paddle:
    def __init__(self):
        self.form = STDRD_SIZE_PADDLE

    def add_special(self, special):
        self.special = special

    def tick(self):
        self.special.time = self.special.time - 1

    def change_size(self):
        pass

    def reset_size(self):
        self.form = STDRD_SIZE_PADDLE

    def move(self):
        pass


class Ball:
    def __init__(self):
        self.form = STNDRD_FORM_BALL

    def add_special(self, special):
        self.special = special

    def tick(self):
        self.special.time = self.special.time - 1

    def move(self):
        pass


class Brick:
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
                - decrement hits_left
                -
        :return:
        """
        self.hits_left -= 1
        return self.hits_left == 0

    def show_brick(self, screen):
        """
            description:
                - select color/background based on self.hits_left
        :return:
        """
        pygame.draw.rect(screen, COLORS_BRICKS[self.hits_left - 1], self.rect)
