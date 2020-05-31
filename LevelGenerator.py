import pygame
from GameElements import  Brick
from DatabaseInteract import  DatabaseInteract

class LevelGenerator():

    def create_level(self, level):
        self.difficulty = DatabaseInteract().get_settings()[7]
        
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
        for __ in range(2):
            x = 347
            for _ in range(4):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        y += 24
        for __ in range(2):
            x = 239
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            x+=27*8
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        y += 24
        for __ in range(2):
            x = 131
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            x+=27*16
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        y += 24
        for __ in range(2):
            x = 23
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            x+=27*24
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
            x = 347
            for _ in range(4):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
        y += 24
        for __ in range(2):
            x = 239
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            x+=27*8
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        y += 24
        for __ in range(2):
            x = 131
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            x+=27*16
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        y += 24

        return blocks
    
    def create_level_2(self):
        y = 50
        blocks = []
        for __ in range(3):
            x = 50
            for _ in range(26):
                block = Brick((x, y), 1+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        
        for __ in range (18):
            x = 50
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            x = 698
            for _ in range(2):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12

        return blocks  

    def create_level_3(self):
        y = 50
        blocks = []
        for __ in range(2):
            x = 347
            for _ in range(4):
                block = Brick((x, y), 2+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(2):
            x = 293
            for _ in range(8):
                block = Brick((x, y), 1+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(2):
            x = 239
            for _ in range(12):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(2):
            x = 185
            for _ in range(16):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(2):
            x = 131
            for _ in range(20):
                block = Brick((x, y), 1+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(2):
            x = 77
            for _ in range(24):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(2):
            x = 131
            for _ in range(20):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(2):
            x = 185
            for _ in range(16):
                block = Brick((x, y), 3+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(2):
            x = 239
            for _ in range(12):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(2):
            x = 293
            for _ in range(8):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(2):
            x = 347
            for _ in range(4):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
            
        return blocks   

    def create_level_4(self):
        y = 50
        blocks = []
        for __ in range(2):
            x = 50
            for _ in range(3): 
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            x+=540
            for _ in range(3): 
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        y += 12 * 6
        for __ in range(2):
            x = 347
            for _ in range(4):
                block = Brick((x, y), 1+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(2):
            x = 293
            for _ in range(8):
                block = Brick((x, y), 1+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(1):
            x = 239
            for _ in range(12):
                block = Brick((x, y), 2+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        for __ in range(1):
            x = 239
            for _ in range(12):
                block = Brick((x, y), -1)
                blocks.append(block)
                x += 27
            y += 12
        return blocks 
             
    def create_level_5(self):
        y = 50
        blocks = []
        for __ in range(2):
            x = 131
            for _ in range(3):
                block = Brick((x, y), 2+self.difficulty)
                blocks.append(block)
                x += 27
            x += 5*27
            for _ in range(4):
                block = Brick((x, y), 1+self.difficulty)
                blocks.append(block)
                x += 27
            x += 5*27
            for _ in range(3):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            x += 5*27
            y += 12
        y+=48
        for __ in range(2):
            x = 77
            for _ in range(3): 
                block = Brick((x, y), -1)
                blocks.append(block)
                x += 27
            x+=3*27
            for _ in range(3): 
                block = Brick((x, y), 6)
                blocks.append(block)
                x += 27
            x+=6*27
            for _ in range(3): 
                block = Brick((x, y), 6)
                blocks.append(block)
                x += 27
            x+=3*27
            for _ in range(3): 
                block = Brick((x, y), 6)
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
                block = Brick((x, y), 6)
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
                block = Brick((x, y), 6)
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
                block = Brick((x, y), 6)
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
                block = Brick((x, y), 6)
                blocks.append(block)
                x += 27
            y += 12
        return blocks  
             
    def create_level_10(self):
        y = 50
        blocks = []

        for __ in range (18):
            x = 50
            for _ in range(3):
                block = Brick((x, y), -1)
                blocks.append(block)
                x += 27
            for _ in range(20):
                block = Brick((x, y), 6)
                blocks.append(block)
                x += 27
            for _ in range(3):
                block = Brick((x, y), -1)
                blocks.append(block)
                x += 27
            y += 12

        for __ in range(3):
            x = 50
            for _ in range(26):
                block = Brick((x, y), -1)
                blocks.append(block)
                x += 27
            y += 12

        return blocks 
         