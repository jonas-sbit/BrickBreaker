import pygame

STDRD_SIZE_PADDLE = [[pygame.Rect(300, 500, 20, 10), 120],
                [pygame.Rect(320, 500, 20, 10),100],
                [pygame.Rect(340, 500, 20, 10),80],
                [pygame.Rect(360, 500, 20, 10),45],
        ]

STNDRD_FORM_BALL = pygame.Rect(300, 490, 5, 5)

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
        

class Ball():
    def __init__(self):
        self.form = STNDRD_FORM_BALL

    def add_special(self, special):
        self.special = special

    def tick(self):
        self.special.time = self.special.time - 1
        
    def move(self):
        pass

class Brick():
    def __init__(self):
        pass
    