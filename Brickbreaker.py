import pygame
from pygame.locals import *
from GameElements import Paddle, Ball, Brick
from LevelGenerator import LevelGenerator
from UIElement import WHITE, BLUE
from GameElements import Movement
from enum import Enum
from DatabaseInteract import DatabaseInteract 
from GameState import GameState
import os

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600


class RectSide(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 3
    RIGHT = 3


class CollisionType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Brickbreaker:
    def __init__(self):
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.bricks = []

        self.paddle = Paddle()
        # TODO: Zufallsstartpunkt?
        self.ball = Ball(self.paddle.hitzones[3][1])

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 25)
        # TODO self.score umbauen auf Player.score
        self.score = 0

    def create_blocks(self):
        self.bricks = LevelGenerator().create_level(1)
        # []
        # y = 50
        # for __ in range(20):
        #     x = 50
        #     for _ in range(26):
        #         block = pygame.Rect(x, y, 25, 10)
        #         self.blocks.append(block)
        #         x += 27
        #     y += 12

    def ball_update(self):
        # idee: x und y bewegung getrennt durchfuehren
        self.ball.move()
        """speed = self.speeds[self.angle]
        xMovement = True
        if _:
            self.ball.x += speed[0] * self.direction
        else:
            self.ball.y += speed[1] * self.direction * self.yDirection
            xMovement = False"""
        # collision left or right edge
        if self.ball.form.x <= 0 or self.ball.form.x >= DISPLAY_WIDTH:
            self.ball.collide_vertical()
            if self.ball.form.x <= 0:
                self.ball.form.x = 1
            else:
                self.ball.form.x = DISPLAY_WIDTH - 1
        # collision top edge
        if self.ball.form.y <= 0:
            self.ball.form.y = 1
            self.ball.collide_horizontal()

        # collission paddle
        for paddle_part in self.paddle.hitzones:
            if paddle_part[0].colliderect(self.ball.form):
                self.ball.vector = paddle_part[1]
                break
        # brick collisions
        collision_bricks = []
        for brick in self.bricks:
            if brick.rect.colliderect(self.ball.form):
                collision_bricks.append(brick)
        if len(collision_bricks) > 0:
            self.handle_brick_collisions(collision_bricks)

        # collision bottom edge --> lost
        if self.ball.form.y > DISPLAY_HEIGHT:
            self.create_blocks()
            self.score = 0
            self.ball.form.x = self.paddle.hitzones[3][0].x
            self.ball.form.y = 490
            self.ball.vector = self.paddle.hitzones[3][1]

    def check_previously_horizontally_outside(self, brick_rect, horizontal_movement):
        """
        description:
            - Check whether the ball did not horizontally overlap with the currently brick hit in the previous frame.
            - Aligned edges do not count as overlap.
        :param brick_rect: pygame.Rect-Object representing the hit brick's position.
        :param horizontal_movement: Movement-Enum value indicating left or right movement
        :return: true if no overlap, false otherwise
        """
        ball_pos_previous = self.ball.get_previous_position()
        ball_rect_previous = pygame.Rect(ball_pos_previous[0], ball_pos_previous[1], self.ball.form.width,
                                         self.ball.form.height)
        if horizontal_movement == Movement.RIGHT:
            return ball_rect_previous.right <= brick_rect.left
        else:
            return ball_rect_previous.left >= brick_rect.right

    def check_previously_vertically_outside(self, brick_rect, vertical_movement):
        """
        description:
            - Check whether the ball did not vertically overlap with the currently brick hit in the previous frame.
            - Aligned edges do not count as overlap.
        :param brick_rect: pygame.Rect-Object representing the hit brick's position.
        :param vertical_movement: Movement-Enum value indicating up or down movement
        :return: true if no overlap, false otherwise
        """
        ball_pos_previous = self.ball.get_previous_position()
        ball_rect_previous = pygame.Rect(ball_pos_previous[0], ball_pos_previous[1], self.ball.form.width,
                                         self.ball.form.height)
        if vertical_movement == Movement.DOWN:
            return ball_rect_previous.bottom <= brick_rect.top
        else:
            return ball_rect_previous.top >= brick_rect.bottom

    def handle_brick_collisions(self, collision_bricks):
        """
        description:
            - Handle the brick-collision based on the number of bricks hit.
            - If only one brick was hit: Call function to perform brick collision with determined collision type
            - More than one (basically working with the first 2,
              edge-case of more than 2 ignored due to unlikelihood and complexity):
                - Determine expected collision type based on the relative position of the 2 bricks.
                - Determine calculated collision type for 2 bricks.
                - Perform brick collision with the brick matching the expected collision type.
                - If none matches: chose one (irrelevant for user experience) to perform the brick collision with using
                  expected collision type.
        :param collision_bricks: list of Brick-objects hit by the ball
        :return: nothing
        """
        if len(collision_bricks) == 1:
            self.perform_brick_collision(collision_bricks[0], self.determine_collision_type(collision_bricks[0]))
        else:
            if collision_bricks[0].rect.x == collision_bricks[1].rect.x:            # above each other
                collision_required = CollisionType.VERTICAL
            else:                                                                   # next to each other
                collision_required = CollisionType.HORIZONTAL
            brick1_collision = self.determine_collision_type(collision_bricks[0])
            brick2_collision = self.determine_collision_type(collision_bricks[1])
            if brick1_collision == collision_required:
                self.perform_brick_collision(collision_bricks[0], brick1_collision)
            elif brick2_collision == collision_required:
                self.perform_brick_collision(collision_bricks[1], brick2_collision)
            else:
                self.perform_brick_collision(collision_bricks[0], collision_required)

    def determine_collision_type(self, brick_hit):
        """
        description:
            - Determine the collision type based on the movement and overlap in the previous frame.
        :param brick_hit: Brick-object determine the theoretical collision type for.
        :return: CollisionType-enum value
        """
        horizontal_movement = self.ball.get_horizontal_movement()
        vertical_movement = self.ball.get_vertical_movement()
        previously_horizontally_outside = self.check_previously_horizontally_outside(brick_hit.rect,
                                                                                     horizontal_movement)
        previously_vertically_outside = self.check_previously_vertically_outside(brick_hit.rect, vertical_movement)

        # neither horizontal nor vertical overlap in the previous frame
        # --> compare ratio of horizontal and vertical overlap in the current frame
        if previously_horizontally_outside and previously_vertically_outside:
            horizontal_delta = (self.ball.form.right - brick_hit.rect.left) if horizontal_movement == Movement.RIGHT \
                else (brick_hit.rect.right - self.ball.form.left)
            vertical_delta = (self.ball.form.bottom - brick_hit.rect.top) if vertical_movement == Movement.DOWN \
                else (brick_hit.rect.bottom - self.ball.form.top)
            if horizontal_delta > vertical_delta:
                return CollisionType.HORIZONTAL
            else:
                return CollisionType.VERTICAL
        # horizontal overlap but no vertical overlap in the previous frame --> vertical collision
        elif previously_horizontally_outside and not previously_vertically_outside:
            return CollisionType.VERTICAL
        # no horizontal overlap but vertical overlap in the previous frame --> horizontal collision
        elif not previously_horizontally_outside and previously_vertically_outside:
            return CollisionType.HORIZONTAL
        # horizontal overlap and vertical overlap in the previous frame
        # --> irrelevant here because collision would have already happended and been handled in the previous frame.

    def perform_brick_collision(self, brick_hit, collision_type):
        """
        description:
            - Call function to change ball's movement direction based on the collision_type.
            - Call Brick's get_hit() function.
            - Destroy brick and increase score if brick was destroyed.
        :param brick_hit: Brick-object to perform the collision with
        :param collision_type: CollisionType-Enum
        :return: nothing
        """
        if collision_type == CollisionType.HORIZONTAL:
            self.ball.collide_horizontal()
        else:
            self.ball.collide_vertical()

        if brick_hit.get_hit():
            self.bricks.remove(brick_hit)
            self.score += 1

    def main(self, buttons):
        # pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        self.create_blocks()
        
        dbi = DatabaseInteract()
        sets = dbi.get_settings()

        key_left = sets[2]
        key_right = sets[4]

        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    os._exit(1)
            keys = pygame.key.get_pressed()
            if keys[int(key_left)]:
                self.paddle.move(-1)
            if keys[int(key_right)]:
                self.paddle.move(1)
            if keys[int(sets[6])]:
                return GameState.TITLE
            if keys[pygame.K_ESCAPE]:
                return GameState.TITLE

            self.screen.fill(BLUE)
            self.ball_update()

            for brick in self.bricks:
                brick.show_brick(self.screen)
            for paddle_part in self.paddle.hitzones:
                pygame.draw.rect(self.screen, WHITE, paddle_part[0])
            for triangle in self.paddle.triangle_views:
                pygame.draw.polygon(self.screen, WHITE, triangle)
            pygame.draw.rect(self.screen, WHITE, self.ball.form)
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
