import pygame
import os
from enum import Enum
from numpy.random import choice

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# Paddle Constants
# each rect 8 wide, speed = 8 and left edge is multiple of 8 to enable across-the-border-movement (Special)
PADDLE_PART_WIDTH = 8
PADDLE_MAX_HEIGHT = 12
PADDLE_TOP_EDGE = 500
PADDLE_SLANTED_DIVISORS = (1.5, 3)      # order: inner to outer slanted part
# standard paddle consisting of 12 rectangles with corresponding bounce-off vector; order left to right
STD_SIZE_PADDLE = [[pygame.Rect(352, PADDLE_TOP_EDGE + PADDLE_MAX_HEIGHT / PADDLE_SLANTED_DIVISORS[0],
                                PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT / PADDLE_SLANTED_DIVISORS[1]), (-5, -1)],
                   [pygame.Rect(360, PADDLE_TOP_EDGE + PADDLE_MAX_HEIGHT / PADDLE_SLANTED_DIVISORS[1],
                                PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT / PADDLE_SLANTED_DIVISORS[0]), (-4, -2)],
                   [pygame.Rect(368, PADDLE_TOP_EDGE, PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT), (-3, -3)],
                   [pygame.Rect(376, PADDLE_TOP_EDGE, PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT), (-2, -4)],
                   [pygame.Rect(384, PADDLE_TOP_EDGE, PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT), (-2, -4)],
                   [pygame.Rect(392, PADDLE_TOP_EDGE, PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT), (-1, -5)],
                   [pygame.Rect(400, PADDLE_TOP_EDGE, PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT), (1, -5)],
                   [pygame.Rect(408, PADDLE_TOP_EDGE, PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT), (2, -4)],
                   [pygame.Rect(416, PADDLE_TOP_EDGE, PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT), (2, -4)],
                   [pygame.Rect(424, PADDLE_TOP_EDGE, PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT), (3, -3)],
                   [pygame.Rect(432, PADDLE_TOP_EDGE + PADDLE_MAX_HEIGHT / PADDLE_SLANTED_DIVISORS[1],
                                PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT / PADDLE_SLANTED_DIVISORS[0]), (4, -2)],
                   [pygame.Rect(440, PADDLE_TOP_EDGE + PADDLE_MAX_HEIGHT / PADDLE_SLANTED_DIVISORS[0],
                                PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT / PADDLE_SLANTED_DIVISORS[1]), (5, -1)]
                   ]
PADDLE_GROWTH_PARTS = [[pygame.Rect(0, PADDLE_TOP_EDGE, PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT), (-1, -5)],
                       [pygame.Rect(0, PADDLE_TOP_EDGE, PADDLE_PART_WIDTH, PADDLE_MAX_HEIGHT), (1, -5)]]
STD_PADDLE_SPEED = 8

# Ball Constants
STD_FORM_BALL = pygame.Rect(315, 490, 5, 5)

# Brick Constants
BRICK_WIDTH = 25
BRICK_HEIGHT = 10
COLOR_UNBREAKABLE_BRICK = (135, 135, 135)

CRNT_PATH = os.path.dirname(__file__)  # Where your .py file is located
BSI_path = os.path.join(CRNT_PATH, 'brick_state_images')  # The Brick State Images folder path

# Special Constants
SPECIAL_WIDTH = 25
SPECIAL_HEIGHT = 10
SPECIAL_COLOR = (135, 135, 135)
SPECIAL_FALL_SPEED = 2
SPECIAL_TTL = 10


class Movement(Enum):
    """ Possible horizontal and vertical movement directions """
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Paddle:
    def __init__(self):
        """
        description:
            - Create a new instance of a Paddle-object.
            - Initialize the paddle's hitzones with the STD_SIZE_PADDLE.
            - Initialize self.triangle_views covering the slanted parts of the paddle.
            - Initialize self.speed with STD_PADDLE_SPEED.
            - Initialize self.special with None as the paddle starts without any specials.
        """
        self.hitzones = STD_SIZE_PADDLE.copy()
        self.triangle_views = self.create_triangles()
        self.speed = STD_PADDLE_SPEED
        self.special = None

    def get_left_edge(self):
        """
        Description:
            - Return the left edge of the whole paddle representation on screen.
        :return: left edge of the paddle
        """
        return self.hitzones[0][0].left

    def get_right_edge(self):
        """
        Description:
            - Return the right edge of the whole paddle representation on screen.
        :return: right edge of the paddle
        """
        return self.hitzones[len(self.hitzones) - 1][0].right

    def get_top_edge(self):
        """
        Description:
            - Return the top edge of the whole paddle representation on screen.
        :return: top edge of the paddle
        """
        top_edge = self.hitzones[0][0].top
        for paddle_part in self.hitzones:
            if paddle_part[0].top < top_edge:
                top_edge = paddle_part[0].top
        return top_edge

    def get_bottom_edge(self):
        """
        Description:
            - Return the bottom edge of the whole paddle representation on screen.
        :return: bottom edge of the paddle
        """
        return self.hitzones[0][0].bottom

    def activate_special(self, special):
        """
        description:
            - Adds the given special to the paddle.
            - If special.type is changing the paddle's size: Call corresponding method.
            - Non-size-changing specials are handled in the methods affected by the special.
        :param special: the special to activate
        :return: nothing
        """
        self.special = special
        if self.special.special_type == SpecialType.BIGGER_PADDLE:
            self.grow()
        elif self.special.special_type == SpecialType.SMALLER_PADDLE:
            self.shrink()

    def remove_special(self):
        """
        description:
            - Remove the special from the paddle and restore the standard paddle state.
        :return: nothing
        """
        if not (self.special is None):
            if self.special.special_type == SpecialType.BIGGER_PADDLE \
                    or self.special.special_type == SpecialType.SMALLER_PADDLE:
                self.reset_size()
            elif self.special.special_type == SpecialType.ACROSS_BORDER:
                if self.get_left_edge() > (DISPLAY_WIDTH / 2) > self.get_right_edge():
                    self.set_position(self.determine_standard_position())
            self.special = None

    def determine_standard_position(self):
        """
        description:
            - Determines whether more parts of the paddle are positioned on the left edge or the right edge
              of the screen when Special.ACROSS_BORDERS ends.
            - If equally distributed: position at left edge of screen.
            - left edge can cause off-screen position
        :return: left edge to position the pedal in standard mode
        """
        counter_right_edge = 0
        counter_left_edge = 0
        for paddle_part in self.hitzones:
            if paddle_part[0].x > DISPLAY_WIDTH / 2:  # positioned at right edge
                counter_right_edge += 1
            else:  # positioned
                counter_left_edge += 1
        if counter_right_edge > counter_left_edge:
            return self.get_left_edge()
        else:
            return self.get_left_edge() - 800

    def grow(self):
        """
        description:
            - Increase the paddle's size by adding two new parts to it in the middle.
            - Align the parts correctly using the left edge of the pedal.
        :return: nothing
        """
        # len(self.hitzones) is always even --> middle addresses element right to the middle
        current_middle = int(len(self.hitzones) / 2)
        self.hitzones.insert(current_middle, PADDLE_GROWTH_PARTS[0])
        self.hitzones.insert(current_middle + 1, PADDLE_GROWTH_PARTS[1])
        self.set_position(self.get_left_edge())

    def shrink(self):
        """
        description:
            - Decrease the paddle's size by removing the middle four parts.
            - Align the remaining parts correctly using the left edge of the pedal.
        :return:
        """
        # len(self.hitzones) is always even --> middle addresses element right to the middle
        current_middle = int(len(self.hitzones) / 2)
        if current_middle >= 3:     # ensure that paddle consists of enough part (should always be the case)
            for i in range(current_middle + 1, current_middle - 3, -1):
                self.hitzones.pop(i)
            self.set_position(self.get_left_edge())

    def reset_size(self):
        """
        description:
            - Restore the standard paddle.
            - Call set_position function with saved left edge of previous position
              to ensure paddle at the same position (left aligned).
        :return: nothing
        """
        left_edge = self.hitzones[0][0].left
        self.hitzones = STD_SIZE_PADDLE.copy()
        self.set_position(left_edge)

    def move(self, direction):
        """
        description
            - Change the paddle's part's x-coordinates to change its position on the screen using self.speed.
            - Movement is checked so the paddle always remains right at the edge of the screen when leaving it.
            - If Special.ACROSS_BORDER is active:
                - Change coordinates of parts leaving the screen to appear on the other side of it.
            - If Special.CONFUSED_CONTROLS is active:
                - Reverse movement direction.
        :param direction: 1 for right-movement, -1 for left-movement
        :return: nothing
        """
        across_edge_special_active = False
        if not (self.special is None):
            if self.special.special_type == SpecialType.CONFUSED_CONTROLS:
                direction *= -1
            elif self.special.special_type == SpecialType.ACROSS_BORDER:
                across_edge_special_active = True

        if not across_edge_special_active:
            if not (self.hitzones[0][0].left + (self.speed * direction)) > DISPLAY_WIDTH and \
                    not (self.hitzones[len(self.hitzones) - 1][0].right + (self.speed * direction)) < 0:
                for paddle_part in self.hitzones:
                    paddle_part[0].x += self.speed * direction
                self.triangle_views = self.create_triangles()
        else:
            for paddle_part in self.hitzones:
                paddle_part[0].x += self.speed * direction
                if direction == 1:                              # right movement
                    if paddle_part[0].left >= DISPLAY_WIDTH:
                        paddle_part[0].x -= DISPLAY_WIDTH
                else:                                           # left movement
                    if paddle_part[0].right <= 0:
                        paddle_part[0].x += DISPLAY_WIDTH
        self.triangle_views = self.create_triangles()

    def set_position(self, left_edge):
        """
        description:
            - Set the position of the paddle by aligning all parts to the given left edge.
        :param left_edge: new left edge of the pedal
        :return: nothing
        """
        i = 0
        for paddle_part in self.hitzones:
            paddle_part[0].x = left_edge + (i * PADDLE_PART_WIDTH)
            i += 1
        self.update_triangles()

    def update_triangles(self):
        """
        description:
            - Update self.triangles_views to the current paddle position by calling self.create_triangles.
        :return: nothing
        """
        self.triangle_views = self.create_triangles()

    def create_triangles(self):
        """
        description:
            - Calculate the tuples / coordinates to draw the triangles (polygons) visually covering up the rectangles
              used to build the slanted parts of the paddle
        :return: tuple of 4 lists containing the tuples / coordinates
        """
        """return ([self.hitzones[0][0].topleft,
                 self.hitzones[2][0].topleft,
                 (self.hitzones[2][0].left, self.hitzones[0][0].y)],
                [self.hitzones[len(self.hitzones) - 1][0].topright,
                 self.hitzones[len(self.hitzones) - 3][0].topright,
                 (self.hitzones[len(self.hitzones) - 3][0].right, self.hitzones[len(self.hitzones) - 1][0].top)])"""
        return ([self.hitzones[0][0].topleft,
                 self.hitzones[0][0].topright,
                (self.hitzones[0][0].right, self.hitzones[1][0].top)],
                [self.hitzones[1][0].topleft,
                 self.hitzones[1][0].topright,
                (self.hitzones[1][0].right, self.hitzones[2][0].top)],
                [self.hitzones[len(self.hitzones) - 1][0].topright,
                 self.hitzones[len(self.hitzones) - 1][0].topleft,
                (self.hitzones[len(self.hitzones) - 1][0].left, self.hitzones[len(self.hitzones) - 2][0].top)],
                [self.hitzones[len(self.hitzones) - 2][0].topright,
                 self.hitzones[len(self.hitzones) - 2][0].topleft,
                (self.hitzones[len(self.hitzones) - 2][0].left, self.hitzones[len(self.hitzones) - 3][0].top)])


class Ball:
    def __init__(self):
        """
        description:
            - Create a new instance of a Ball-object.
            - Initialize rectangle represenation.
            - Initialize movement vector.
        :param vector: tuple representing the horizontal and vertical movement directions of the ball.
        """
        self.form = STD_FORM_BALL.copy()
        self.vector = (0, 0)

    def get_horizontal_movement(self):
        """
        description:
            - Get the direction of the movement in horizontal direction based on self.vector.
        :return: Movement-enum value Movement.LEFT or Movement.RIGHT
        """
        if self.vector[0] > 0:
            return Movement.RIGHT
        else:
            return Movement.LEFT

    def get_vertical_movement(self):
        """
        description:
            - Get the direction of the movement in horizontal direction based on self.vector.
        :return: Movement-enum value Movement.DOWN or Movement.UP
        """
        if self.vector[1] > 0:
            return Movement.DOWN
        else:
            return Movement.UP

    def move(self):
        """
        description:
            - Move the rectangle self.form by adding vector values to current coordinates.
        :return: nothing
        """
        self.form.x += self.vector[0]
        self.form.y += self.vector[1]

    def get_previous_position(self):
        """
        description:
            - Get the ball's position in the previous frame
              by subtracting the vector values from the current coordinates.
        :return: tuple (x, y) representing the position of the ball in the previous frame.
        """
        return self.form.x - self.vector[0], self.form.y - self.vector[1]

    def collide_horizontal(self):
        """
        description:
            - Simulate a collision with a horizontal edge by reversion self.vector's y-coordinate.
        :return: nothing
        """
        self.vector = (self.vector[0], self.vector[1] * -1)

    def collide_vertical(self):
        """
        description:
            - Simulate a collision with a vertical edge by reversing self.vector's x-coordinate.
        :return: nothing
        """
        self.vector = (self.vector[0] * -1, self.vector[1])


class Brick:
    brick_state_images = [pygame.image.load(os.path.join(BSI_path, 'brick_state_0.png')),
                          pygame.image.load(os.path.join(BSI_path, 'brick_state_1.png')),
                          pygame.image.load(os.path.join(BSI_path, 'brick_state_2.png')),
                          pygame.image.load(os.path.join(BSI_path, 'brick_state_3.png'))]

    def __init__(self, coordinates, max_hits):
        """
            description:
                - creates a new object of the brick class
            :param max_hits: number of times the brick has to get hit in order to get destroyed; -1 for unbreakable brick
            :param coordinates: a tuple containing the x- and y-coordinate of the brick's starting point
        """
        self.rect = pygame.Rect(coordinates[0], coordinates[1], BRICK_WIDTH, BRICK_HEIGHT)
        self.hits_left = max_hits if max_hits <= 4 else 4

    def get_hit(self):
        """
        description:
            - Decrement hits_left if brick is not unbreakable (i.e. hits_left = -1).
        :return: boolean whether hits_left was decremented to 0, i.e. brick is destroyed
        """
        if self.hits_left > 0:
            self.hits_left -= 1
        return self.hits_left == 0

    def show_brick(self, screen):
        """
        description:
            - Select color/background based on self.hits_left.
        :param screen: the screen to show the brick on.
        :return: nothing
        """

        if self.hits_left == -1:
            pygame.draw.rect(screen, COLOR_UNBREAKABLE_BRICK, self.rect)
        else:
            screen.blit(self.brick_state_images[self.hits_left - 1], self.rect)


class Special:

    def __init__(self, start_coordinates, special_type):
        """
        description:
            - Create a new object of the special class.
        :param start_coordinates: a tuple containing the x- and y-coordinate of the special's starting point
        :param type: SpecialType-enum value indicating the type that was created.
        """
        self.rect = pygame.Rect(start_coordinates[0], start_coordinates[1], SPECIAL_WIDTH, SPECIAL_HEIGHT)
        self.special_type = special_type
        self.ttl = 0

    def show_special(self, screen):
        """
        description:
            - Draw the special's rect representation to the screen.
        :param screen: the screen to draw the special on
        :return:
        """
        # TODO: color based on negative positive neutral -> in konstanten festlegen und per if ... in ... entscheiden
        pygame.draw.rect(screen, SPECIAL_COLOR, self.rect)

    def fall(self):
        """
        description:
            - move the special's rectangle representation downwards using SPECIAL_FALL_SPEED
        :return:
        """
        self.rect.y += SPECIAL_FALL_SPEED

    def is_paddle_special(self):
        """
        description:
            - Checks whether the Special is a special changing the paddle's behaviour.
        :return: boolean whether the special changes the paddle's behaviour or not
        """
        paddle_specials = (2, 3, 4, 5)  #TODO: in Konstante (in diesem file)
        if self.special_type.value in paddle_specials:
            return True
        else:
            return False

    def activate(self, clock_speed):
        """
        description:
            - Initialize the time to live based on the clock speed in order for the special to stay alive
              for the same timespan no matter the clock speed.
        :param clock_speed:
        :return: nothing
        """
        self.ttl = clock_speed * SPECIAL_TTL

    def tick(self):
        """
        description:
            - Decrement object's time to live.
        :return: boolean whether the ttl was decremented to 0, i.e. is no longer active
        """
        self.ttl -= 1
        return self.ttl == 0


class SpecialType(Enum):
    """ Different specials that can occur during the game. """
    FASTER = 0
    SLOWER = 1
    BIGGER_PADDLE = 2
    SMALLER_PADDLE = 3
    CONFUSED_CONTROLS = 4
    ACROSS_BORDER = 5
    BONUS_LIFE = 6


def choose_random_special():
    """
    description:
        - Choose a random special type from all possible types with defined probabilities.
    :return: randomly selected SpecialType-enum value
    """
    c = choice([    # TODO: TODO: in Konstante (in diesem file)
        SpecialType.FASTER,
        SpecialType.SLOWER,
        SpecialType.BIGGER_PADDLE,
        SpecialType.SMALLER_PADDLE,
        SpecialType.CONFUSED_CONTROLS,
        SpecialType.ACROSS_BORDER,
        SpecialType.BONUS_LIFE],
        1,
        p=[ # TODO: in Konstante (in diesem file)
            0.15,
            0.15,
            0.15,
            0.15,
            0.15,
            0.15,
            0.1
        ]
    )
    return c[0]


def to_drop_special():
    """
    description:
        - Decides whether to drop a special after a brick was destroyed using defined probabilities.
    :return: Boolean whether to drop or not to drop a special
    """
    c = choice([False, True], 1, p=[0.8, 0.2])  # Hier WSLKT Anpassen falls zu viele / wenige Powerups kommen TODO: in Konstante (in diesem file)
    return c[0]
