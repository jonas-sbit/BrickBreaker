import pygame
from enum import Enum
from pygame.sprite import RenderUpdates
from Player import Player
from UIElement import UIElement, BLUE, WHITE
from Breakout import Breakout


class Pages():
    
    def title_screen(self, screen):
        start_btn = UIElement(
            center_position=(500, 300),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Start",
            action=GameState.NEWGAME,
        )
        highscore_btn = UIElement(
            center_position=(500, 400),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Highscores",
            action=GameState.HIGHSCORE,
        )
        quit_btn = UIElement(
            center_position=(500, 500),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Quit",
            action=GameState.QUIT,
        )

        buttons = RenderUpdates(start_btn, quit_btn, highscore_btn)

        return self.game_loop(screen, buttons, 0)

    def play_level(self, screen, player):
        return_btn = UIElement(
            center_position=(140, 570),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Return to main menu",
            action=GameState.TITLE,
        )

        nextlevel_btn = UIElement(
            center_position=(400, 400),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Next level ({player.current_level + 1})",
            action=GameState.NEXT_LEVEL,
        )

        buttons = RenderUpdates(return_btn, nextlevel_btn)

        return self.game_loop(screen, buttons, 1)

    def highscore_page(self, screen, player):
        return_btn = UIElement(
            center_position=(140, 570),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Return to main menu",
            action=GameState.TITLE,
        )

        buttons = RenderUpdates(return_btn)

        return self.game_loop(screen, buttons, 0)

    def game_loop(self,screen, buttons, level):
        """ Handles game loop until an action is return by a button in the
            buttons sprite renderer.
        """
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            screen.fill(BLUE)

            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    return ui_action

            buttons.draw(screen)

            if level == 1:
                Breakout().main(buttons)

            pygame.display.flip()

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2
    HIGHSCORE = 3