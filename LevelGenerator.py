import pygame
from GameElements import  Brick

class LevelGenerator():
# TODO Wenn Klasse Brick fertig ist, umbauen auf Bricks und Level anhand von Mockups programmieren

    def create_level(self, level):
        switcher = {
            1:  self.create_level_1(),
            2:  self.create_level_2(),
            3:  self.create_level_3(),
            4:  self.create_level_4(),
            5:  self.create_level_5(),
            6:  self.create_level_6(),
            7:  self.create_level_7(),
            8:  self.create_level_8(),
            9:  self.create_level_9(),
            10:  self.create_level_10()
        }
        return switcher.get(level, self.create_level_1())

    def create_level_1(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 50
            for _ in range(26):
                block = pygame.Rect(x, y, 25, 10)
                blocks.append(block)
                x += 27
            y += 12
        return blocks
    
    def create_level_2(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 50
            for _ in range(26):
                block = pygame.Rect(x, y, 25, 10)
                blocks.append(block)
                x += 27
            y += 12
        return blocks  

    def create_level_3(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 50
            for _ in range(26):
                block = pygame.Rect(x, y, 25, 10)
                blocks.append(block)
                x += 27
            y += 12
        return blocks   

    def create_level_4(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 50
            for _ in range(26):
                block = pygame.Rect(x, y, 25, 10)
                blocks.append(block)
                x += 27
            y += 12
        return blocks   
             
    def create_level_5(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 50
            for _ in range(26):
                block = pygame.Rect(x, y, 25, 10)
                blocks.append(block)
                x += 27
            y += 12
        return blocks   
             
    def create_level_6(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 50
            for _ in range(26):
                block = pygame.Rect(x, y, 25, 10)
                blocks.append(block)
                x += 27
            y += 12
        return blocks   
             
    def create_level_7(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 50
            for _ in range(26):
                block = pygame.Rect(x, y, 25, 10)
                blocks.append(block)
                x += 27
            y += 12
        return blocks   
             
    def create_level_8(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 50
            for _ in range(26):
                block = pygame.Rect(x, y, 25, 10)
                blocks.append(block)
                x += 27
            y += 12
        return blocks   
             
    def create_level_9(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 50
            for _ in range(26):
                block = pygame.Rect(x, y, 25, 10)
                blocks.append(block)
                x += 27
            y += 12
        return blocks   
             
    def create_level_10(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 50
            for _ in range(26):
                block = pygame.Rect(x, y, 25, 10)
                blocks.append(block)
                x += 27
            y += 12
        return blocks   
         