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
        bricks = switcher.get(level, self.create_level_1())
        unbreakable_bricks = 0
        for brick in bricks:
            if brick.hits_left == -1:           # unbreakable
                unbreakable_bricks += 1
        return bricks, unbreakable_bricks

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
                block = Brick((x, y), 2+self.difficulty)
                blocks.append(block)
                x += 27
            x+=6*27
            for _ in range(3): 
                block = Brick((x, y), 2+self.difficulty)
                blocks.append(block)
                x += 27
            x+=3*27
            for _ in range(3): 
                block = Brick((x, y), 2+self.difficulty)
                blocks.append(block)
                x += 27
            y += 12
        y+=48
        for __ in range(2):
            x = 131
            for _ in range(3):
                block = Brick((x, y), -1)
                blocks.append(block)
                x += 27
            x += 14*27
            for _ in range(3):
                block = Brick((x, y), 0+self.difficulty)
                blocks.append(block)
                x += 27
            x += 5*27
            y += 12
        y+=48
        for __ in range(2):
            x = 239            
            for _ in range(3): 
                block = Brick((x, y), -1)
                blocks.append(block)
                x += 27
            x+=6*27
            for _ in range(3): 
                block = Brick((x, y), 2+self.difficulty)
                blocks.append(block)
                x += 27
            x+=3*27
            y += 12
        y+=48    
        for __ in range(2):
            x = 347
            for _ in range(4):
                if _ < 2:
                    block = Brick((x, y), -1)
                else:
                    block = Brick((x, y), 1+self.difficulty)
                blocks.append(block)
                x += 27
            x += 5*27
            y += 12
        y+=48        

        return blocks 
             
    def create_level_6(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 347
            if __ < 4 or __ > 16:
                for _ in range(4):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27
            else:
                for _ in range(4):
                    block = Brick((x, y), 1+self.difficulty)
                    blocks.append(block)
                    x += 27
            y += 12
            
            if __ > 3 and __ < 6:
                x = 239
                for _ in range(2):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27
                x += 8*27
                for _ in range(2):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27
            
            if __ > 6 and __ < 9:
                x = 131
                for _ in range(2):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27
                x += 16*27
                for _ in range(2):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27

            if __ > 9 and __ < 12:
                x = 23
                for _ in range(2):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27
                x += 24*27
                for _ in range(2):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27

        return blocks    
             
    def create_level_7(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 239
            if __ < 3:
                for _ in range(2):
                    block = Brick((x, y), 0 + self.difficulty)
                    blocks.append(block)
                    x += 27
                x+=9*27
                for _ in range(2):
                    block = Brick((x, y), 0 + self.difficulty)
                    blocks.append(block)
                    x += 27
            elif __ < 5:
                x = 131
                for _ in range(2):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27
                for _ in range(2):
                    block = Brick((x, y), 0 + self.difficulty)
                    blocks.append(block)
                    x += 27
                x+=13*27
                for _ in range(2):
                    block = Brick((x, y), 0 + self.difficulty)
                    blocks.append(block)
                    x += 27
                for _ in range(2):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27
            elif __ < 7:
                x = 131
                for _ in range(2):
                    block = Brick((x, y), 0+self.difficulty)
                    blocks.append(block)
                    x += 27
                for _ in range(2):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27
                x+=13*27
                for _ in range(2):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27
                for _ in range(2):
                    block = Brick((x, y), 0+self.difficulty)
                    blocks.append(block)
                    x += 27
            elif __ < 9:
                x = 77
                for _ in range(2):
                    block = Brick((x, y), 0+self.difficulty)
                    blocks.append(block)
                    x += 27
                x+=21*27
                for _ in range(2):
                    block = Brick((x, y), 0+self.difficulty)
                    blocks.append(block)
                    x += 27
            elif __ < 11:
                x = 320
                for _ in range(7):
                    block = Brick((x, y), 0+self.difficulty)
                    blocks.append(block)
                    x += 27                      
            elif __ < 12:
                x = 50
                for _ in range(1):
                    block = Brick((x, y), 0+self.difficulty)
                    blocks.append(block)
                    x += 27
                x = 293
                for _ in range(9):
                    block = Brick((x, y), -1)
                    blocks.append(block)
                    x += 27
                x = 752
                for _ in range(1):
                    block = Brick((x, y), 0+self.difficulty)
                    blocks.append(block)
                    x += 27
            elif __ < 19:
                x = 50
                for _ in range(1):
                    block = Brick((x, y), 0+self.difficulty)
                    blocks.append(block)
                    x += 27
                x = 752
                for _ in range(1):
                    block = Brick((x, y), 0+self.difficulty)
                    blocks.append(block)
                    x += 27 

            y+=12
        return blocks  
             
    def create_level_8(self):
        y = 50
        blocks = []
        for __ in range(20):
            x = 347
            if __ < 3:
                for _ in range(4):
                    block = Brick((x, y), 0 + self.difficulty)
                    blocks.append(block)
                    x += 27
            elif __ < 8 :
                x = 131
                for _ in range(20):
                    block = Brick((x, y), 0 + self.difficulty)
                    blocks.append(block)
                    x += 27
            elif __ < 12 :
                x = 239
                for _ in range(12):
                    if _ < 4:
                        block = Brick((x, y), -1)
                        blocks.append(block)
                    elif _ > 7:
                        block = Brick((x, y), -1)
                        blocks.append(block)
                    else:
                        block = Brick((x, y), 0 + self.difficulty)
                        blocks.append(block)
                    x += 27
            elif __ < 14 :
                x = 374
                for _ in range(2):
                    block = Brick((x, y), 0 + self.difficulty)
                    blocks.append(block)
                    x += 27
            elif __ < 15:
                x = 131
                blocks.append(Brick((x, y), -1))
                x += 27 * 19
                blocks.append(Brick((x, y), -1))

            y += 12
        return blocks   
             
    def create_level_9(self): # Ab level 9 Schwierigkeit egal
        y = 50
        blocks = []
        for __ in range(20):
            x = 50
            if __ < 2:
                for _ in range(26):
                    block = Brick((x, y), 6)
                    blocks.append(block)
                    x += 27

            elif __ < 4:
                for _ in range(26):
                    if _ < 7 or _ > 18:
                        block = Brick((x, y), 6)
                        blocks.append(block)
                    elif _ < 19:
                        block = Brick((x, y), -1)
                        blocks.append(block)
                    x += 27

            elif __ < 6:
                for _ in range(26):
                    if _ < 5 or _ > 20:
                        block = Brick((x, y), 6)
                        blocks.append(block)
                    elif _ < 21:
                        block = Brick((x, y), -1)
                        blocks.append(block)
                    x += 27

            elif __ < 8:
                for _ in range(26):
                    if _ < 3 or _ > 22:
                        block = Brick((x, y), 6)
                        blocks.append(block)
                    elif _ < 23:
                        block = Brick((x, y), -1)
                        blocks.append(block)
                    x += 27

            elif __ < 10:
                for _ in range(26):
                    if _ < 1 or _ > 24:
                        block = Brick((x, y), 6)
                        blocks.append(block)
                    elif _ < 25:
                        block = Brick((x, y), -1)
                        blocks.append(block)
                    x += 27

            elif __ < 12:
                for _ in range(26):
                    block = Brick((x, y), -1)
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
         