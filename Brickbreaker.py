import pygame
from pygame.locals import *
from GameElements import Paddle, Ball, Brick
from LevelGenerator import LevelGenerator
from UIElement import WHITE, BLUE
import os



class Brickbreaker:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.bricks = []

        ball = Ball()
        self.paddle = Paddle()
        self.ball = ball.form

        self.direction = -1
        self.yDirection = -1
        self.angle = 80

        self.speeds = {
            120:(-10, -3),
            100:(-10, -8),
            80:(10, -8),
            45:(10, -3),
        }
        self.swap = {
            120:45,
            45:120,
            100:80,
            80:100,
        }
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 25)
        # TODO self.score umbauen auf Player.score
        self.score = 0

    def createBlocks(self):
        self.bricks = LevelGenerator().create_level(4)
        # []
        # y = 50
        # for __ in range(20):
        #     x = 50
        #     for _ in range(26):
        #         block = pygame.Rect(x, y, 25, 10)
        #         self.blocks.append(block)
        #         x += 27
        #     y += 12

    def ballUpdate(self):
        for _ in range(2):
            speed = self.speeds[self.angle]
            xMovement = True
            if _:
                self.ball.x += speed[0] * self.direction
            else:
                self.ball.y += speed[1] * self.direction * self.yDirection
                xMovement = False
            if self.ball.x <= 0 or self.ball.x >= 800:
                self.angle = self.swap[self.angle]
                if self.ball.x <= 0:
                    self.ball.x = 1
                else:
                    self.ball.x = 799
            if self.ball.y <= 0:
                self.ball.y = 1
                self.yDirection *= -1
            
            for paddle_part in self.paddle.hitzones:
                if paddle_part[0].colliderect(self.ball):
                    self.angle = paddle_part[1]
                    self.direction = -1
                    self.yDirection = -1
                    break

            for brick in self.bricks:
                if brick.rect.colliderect(self.ball):
                    if brick.get_hit():
                        self.bricks.remove(brick)
                    if xMovement:
                        self.direction *= -1
                    self.yDirection *= -1
                    self.score += 1

            if self.ball.y > 600:
                self.createBlocks()
                self.score = 0
                self.ball.x = self.paddle.hitzones[1][0].x
                self.ball.y = 490
                self.yDirection = self.direction = -1
                
    def paddle_update(self):
        pos = pygame.mouse.get_pos()
        previous_pedal_parts_width_sum = 0
        for p in self.paddle.hitzones:
            p[0].x = pos[0] + previous_pedal_parts_width_sum
            previous_pedal_parts_width_sum += p[0].width
        self.paddle.update_triangles()

    def main(self, buttons):
        #pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        self.createBlocks()
        
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True

            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    os._exit(1)

            self.screen.fill(BLUE)
            self.paddle_update()
            self.ballUpdate()

            for brick in self.bricks:
                brick.show_brick(self.screen)
            for paddle_part in self.paddle.hitzones:
                pygame.draw.rect(self.screen, WHITE, paddle_part[0])
            for triangle in self.paddle.triangles_view:
                pygame.draw.polygon(self.screen, WHITE, triangle)
            pygame.draw.rect(self.screen, WHITE, self.ball)
            self.screen.blit(self.font.render(str(self.score), -1, WHITE), (400, 550))
            
            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    if ui_action.value == -1:
                        pygame.quit()
                        return
                    
                    #if ui_action.value == 0:
                        #TODO zuruek zu title screen
                        #title_screen(pygame.display.set_mode((1000, 750)))
                    
                    return ui_action

            buttons.draw(self.screen)

            pygame.display.update()
