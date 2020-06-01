import pygame
import os
from Constants import DISPLAY_WIDTH, DISPLAY_HEIGHT

LIFE_IMG_WIDTH = 17
LIFE_IMG_HEIGHT = 14
LIFE_IMG_BOTTOM_MARGIN = 5
LIFE_IMG_RIGHT_MARGIN = 5
CRNT_PATH = os.path.dirname(__file__)


class Player:
    """ Stores information about the current player player """

    life_img = pygame.image.load(os.path.join(CRNT_PATH, 'life_img.png'))

    def __init__(self, score=0, lives=3, current_level=1):
        self.score = score
        self.lives = lives
        self.current_level = current_level

    def draw_lives(self, screen):
        """
        description:
            - Draw a heart image to the bottom lef of the screen for every remaining life.
            - Use defined margins and dimensions for proper alignment.
        :param screen: the screen to draw the images on
        :return: nothing
        """
        for i in range(1, self.lives + 1):
            tmp_rect = pygame.Rect(DISPLAY_WIDTH - i * LIFE_IMG_RIGHT_MARGIN - i * LIFE_IMG_WIDTH,
                                   DISPLAY_HEIGHT - LIFE_IMG_BOTTOM_MARGIN - LIFE_IMG_HEIGHT,
                                   LIFE_IMG_WIDTH,
                                   LIFE_IMG_HEIGHT)
            screen.blit(self.life_img, tmp_rect)
