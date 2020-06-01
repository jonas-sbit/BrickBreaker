import pygame
from pygame.locals import *
from GameElements import Paddle, Ball, Brick, Special, \
    SpecialType, to_drop_special, choose_random_special, BOUNCE_OFF_VECTORS
from Player import Player
from LevelGenerator import LevelGenerator
from UIElement import WHITE, BLUE
from GameElements import Movement
from enum import Enum
from DatabaseInteract import DatabaseInteract 
from GameState import GameState
import os

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
DEFAULT_CLOCK_SPEED = 60
CLOCK_SPEED_CHANGE_FACTOR = 1.5


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
        self.clock_speed = DEFAULT_CLOCK_SPEED
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.bricks = []
        self.paddle = Paddle()
        self.ball = Ball()
        self.present_specials = []
        self.active_special = None

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 25)
        # TODO: mit schwierigkeitsgrad startleben bestimmen, ggf. stand laden
        self.player = Player()

    def start_game(self):
        self.create_blocks()
        self.paddle.reset_position()
        # TODO: paddle zu default position (mittig) positionieren
        self.reset_ball()

    def reset_ball(self):
        if not (self.active_special is None):
            self.remove_special()
        vector_indicator_start = self.paddle.get_center()
        for vector in BOUNCE_OFF_VECTORS:
            vector_indicator_end = (vector_indicator_start[0] + 2 * vector[0], vector_indicator_start[1] + 2 * vector[1])
            pygame.draw.line(self.screen, WHITE, vector_indicator_start, vector_indicator_end)
        # TODO: Winkel beim start, ball in mitte positionieren, loop bis leertaste gedrueckt, ggf. hinweis fuer controls
        self.ball.form.x = self.paddle.hitzones[3][0].x
        self.ball.form.y = 490
        self.ball.vector = self.paddle.hitzones[3][1]

    def create_blocks(self):
        """
        description:
            - Create the bricks for the given level using the LevelGenerator-Class
        :param level: number of the level to create
        :return: nothing
        """
        self.bricks = LevelGenerator().create_level(self.player.current_level) # TODO: anpassen

    def check_ball_collisions(self):
        """
        description:
            - Checks all possible collisions that can occur for the ball.
            - Bounce off at left, right and top edge.
            - Bounce off from paddle using paddle.hitzones' vectors.
            - Check for brick collision and delegate handling.
            - TODO: Check win condition --> next level
            - Check if player dropped the ball.
                - TODO: Decrease lifes
                - if decremented to 0 --> game over --> save score
        :return:
        """
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
            self.player.lives -= 1
            if self.player.lives == 0:
                # TODO: save score
                self.player.lives = 3 # TODO: an schwierigkeitsgrad anpassen
                self.player.score = 0
                self.player.current_level = 1
                self.create_blocks()
            self.reset_ball()

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
            - Destroy brick, increase score if brick was destroyed and create a special with a certain probability.
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
            self.player.score += 1
            if to_drop_special():
                self.present_specials.append(Special(brick_hit.rect.topleft, choose_random_special()))

    def check_special_collisions(self):
        """
        description:
            - Check if any specials, i.e. special.rect, currently present on the screen is caught with the paddle.
            - To be caught the special has to be completely within the paddle's horizontal width and the paddle's
              height.
                - Remove active special if new special is caught.
                - Activate special on self or paddle based on its type.
                - Remove the special from the currently present specials and set self.active special.
            - If special is off screen, remove it.
        :return: nothing
        """
        if len(self.present_specials) > 0:
            for special in self.present_specials:
                if (self.paddle.get_top_edge() < special.rect.bottom <= self.paddle.get_bottom_edge()) \
                        and self.paddle.get_left_edge() <= special.rect.left \
                        and self.paddle.get_right_edge() >= special.rect.right:
                    if not (self.active_special is None):
                        self.remove_special()
                    if special.is_paddle_special():
                        self.paddle.activate_special(special)
                    else:
                        self.activate_special(special)
                    self.present_specials.remove(special)
                    self.active_special = special
                    self.active_special.activate(self.clock_speed)
                    print(self.active_special.special_type)
                elif special.rect.top > DISPLAY_HEIGHT:
                    self.present_specials.remove(special)

    def activate_special(self, special):
        """
        description:
            - Activate a caught non-paddle special.
            - Either add a bonus life or adjust clock speed based on special.type
        :param special: the caught special
        :return: nothing
        """
        if special.special_type == SpecialType.BONUS_LIFE:
            self.player.lives += 1
        elif special.special_type == SpecialType.FASTER:
            self.clock_speed = DEFAULT_CLOCK_SPEED * CLOCK_SPEED_CHANGE_FACTOR
        elif special.special_type == SpecialType.SLOWER:
            self.clock_speed = DEFAULT_CLOCK_SPEED / CLOCK_SPEED_CHANGE_FACTOR

    def remove_special(self):
        """
        description:
            - Remove the currently active special and negate its effect.
            - If is_paddle_special: remove special from pedal
            - else: reset self.clock_speed
        :return: nothing
        """
        if self.active_special.is_paddle_special():
            self.paddle.remove_special()
        else:
            self.clock_speed = DEFAULT_CLOCK_SPEED
        self.active_special = None

    def main(self, buttons):
        # pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        self.start_game()
        
        dbi = DatabaseInteract()
        sets = dbi.get_settings()

        key_left = sets[2]
        key_right = sets[4]

        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True

            clock.tick(self.clock_speed)

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
            # update ball
            self.ball.move()
            self.check_ball_collisions()
            # update specials
            if not (self.active_special is None):
                if self.active_special.tick():
                    self.remove_special()
            self.check_special_collisions()

            # Update screen
            for brick in self.bricks:
                brick.show_brick(self.screen)
            for paddle_part in self.paddle.hitzones:
                pygame.draw.rect(self.screen, WHITE, paddle_part[0])
            for triangle in self.paddle.triangle_views:
                pygame.draw.polygon(self.screen, WHITE, triangle)
            for special in self.present_specials:
                special.fall()
                special.show_special(self.screen)
            self.player.draw_lives(self.screen)
            pygame.draw.rect(self.screen, WHITE, self.ball.form)
            self.screen.blit(self.font.render(str(self.player.score), -1, WHITE), (400, 550))

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
