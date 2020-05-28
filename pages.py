import pygame
from enum import Enum
from pygame.sprite import RenderUpdates
from Player import Player
from UIElement import UIElement, BLUE, WHITE, TextElement
from DatabaseInteract import DatabaseInteract
from Brickbreaker import Brickbreaker

MAXIMUM_DIFFICULTY = 4
MINIMUM_DIFFICULTY = 1

class Pages():
    
    def title_screen(self, screen):
        start_btn = UIElement(
            center_position=(400, 100),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Start",
            action=GameState.NEWGAME,
        )
        highscore_btn = UIElement(
            center_position=(400, 200),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Highscores",
            action=GameState.HIGHSCORE,
        )
        settings_btn = UIElement(
            center_position=(400, 300),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Einstellungen",
            action=GameState.SETTINGS,
        )
        quit_btn = UIElement(
            center_position=(400, 400),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Beenden",
            action=GameState.QUIT,
        )

        buttons = RenderUpdates(start_btn, quit_btn, settings_btn, highscore_btn)

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

    def settings_page(self, screen, player):
        # Datenbank zum auslesen der aktuellen Einstellungen
        dbi = DatabaseInteract()
        sets = dbi.get_settings()

        heading = TextElement(
            center_position=(400, 80),
            font_size=25,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Settings",
        )
        return_btn = UIElement(
            center_position=(140, 570),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Return to main menu",
            action=GameState.TITLE,
        )

        move_left = UIElement(
            center_position=(250, 150),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Nach Links: {sets[1]}",
            action=GameState.SETTINGS_HIGHLITED_MOVE_LEFT,
        ) 

        move_right = UIElement(
            center_position=(250, 200),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Nach Rechts: {sets[2]}",
            action=GameState.SETTINGS_HIGHLITED_MOVE_RIGHT,
        )     

        do_pause = UIElement(
            center_position=(250, 250),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Pausenmenü: {sets[3]}",
            action=GameState.SETTINGS_HIGHLITED_DO_PAUSE,
        )    

        difficulty = UIElement(
            center_position=(250, 300),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Schwierigkeit: {sets[4]}",
            action=GameState.SETTINGS_HIGHLITED_DIFFICULTY,
        )     

        buttons = RenderUpdates(return_btn, move_left, move_right, do_pause, difficulty, heading)

        return self.game_loop(screen, buttons, 0)

    def settings_page_highlited(self, screen, player, highlited_btn):
        # Datenbank zum auslesen der aktuellen Einstellungen
        # ansicht der Settings seite zum Auswaehlen des Buttons L/R/Pause 
        dbi = DatabaseInteract()
        sets = dbi.get_settings()

        heading = TextElement(
            center_position=(400, 80),
            font_size=25,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Settings",
        )
        return_btn = UIElement(
            center_position=(140, 570),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Return to main menu",
            action=GameState.TITLE,
        )

        move_left = TextElement(
            center_position=(250, 150),
            font_size=font_size_picker("move_left", highlited_btn),
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Nach Links: {sets[1]}",
        ) 

        move_right = TextElement(
            center_position=(250, 200),
            font_size=font_size_picker("move_right", highlited_btn),
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Nach Rechts: {sets[2]}",
        )     

        do_pause = TextElement(
            center_position=(250, 250),
            font_size=font_size_picker("do_pause", highlited_btn),
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Pausenmenü: {sets[3]}",
        )    

        if highlited_btn !=4 :
            difficulty = TextElement(
                center_position=(250, 300),
                font_size=font_size_picker("difficulty", highlited_btn),
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text=f"Schwierigkeit: {sets[4]}",
            )
        else:
            difficulty = TextElement(
                center_position=(300, 300),
                font_size=font_size_picker("difficulty", highlited_btn),
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text=f"Schwierigkeit: {sets[4]} (mit '+' und '-' anpassen)",
            )


        buttons = RenderUpdates(return_btn, move_left, move_right, do_pause, difficulty, heading)

        return self.game_loop(screen, buttons, highlited_btn * -1)

    def game_loop(self,screen, buttons, level):
        """ Handles game loop until an action is return by a button in the
            buttons sprite renderer.
        """
        dbi = DatabaseInteract()
        sets = dbi.get_settings()

        while True:
            mouse_up = False

            if level < 0:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return GameState.SETTINGS                           
                        if level == -1:
                            if event.unicode != sets[2] and event.unicode != sets[3]:
                                dbi.update_move_left(event.unicode)
                        elif level == -2:
                            if event.unicode != sets[1] and event.unicode != sets[3]:
                                dbi.update_move_right(event.unicode)
                        elif level == -3:
                            if event.unicode != sets[1] and event.unicode != sets[2]:
                                dbi.update_do_pause(event.unicode)
                        elif level == -4:
                            if event.key == 270 or event.key == 93:
                                if(sets[4] < MAXIMUM_DIFFICULTY):
                                    dbi.update_difficulty(sets[4] + 1)
                            elif event.key == 47 or event.key == 269:
                                if(sets[4] > MINIMUM_DIFFICULTY):
                                    dbi.update_difficulty(sets[4] - 1)

                        return GameState.SETTINGS

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        mouse_up = True
            else:
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
                Brickbreaker().main(buttons)

            pygame.display.flip()

    def game_state_logic(self, game_state, screen, player):
        if game_state == GameState.TITLE:
            game_state = self.title_screen(screen)

        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = self.play_level(screen, player)            

        if game_state == GameState.NEXT_LEVEL:
            player.current_level += 1
            game_state = self.play_level(screen, player)

        if game_state == GameState.HIGHSCORE:
            game_state = self.highscore_page(screen, player)

        if game_state == GameState.SETTINGS:
            game_state = self.settings_page(screen, player)

        if game_state == GameState.SETTINGS_HIGHLITED_MOVE_LEFT:
            game_state = self.settings_page_highlited(screen, player, 1)

        if game_state == GameState.SETTINGS_HIGHLITED_MOVE_RIGHT:
            game_state = self.settings_page_highlited(screen, player, 2)

        if game_state == GameState.SETTINGS_HIGHLITED_DO_PAUSE:
            game_state = self.settings_page_highlited(screen, player, 3)

        if game_state == GameState.SETTINGS_HIGHLITED_DIFFICULTY:
            game_state = self.settings_page_highlited(screen, player, 4)

        if game_state == GameState.QUIT:
            game_state = GameState.QUIT

        return game_state

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2
    HIGHSCORE = 3
    SETTINGS = 4
    SETTINGS_HIGHLITED_MOVE_LEFT = 5
    SETTINGS_HIGHLITED_MOVE_RIGHT = 6
    SETTINGS_HIGHLITED_DO_PAUSE = 7
    SETTINGS_HIGHLITED_DIFFICULTY = 8
    

def font_size_picker(button_name, input):
    if button_name == "move_left" and input == 1:
        return 20*1.2
    elif button_name == "move_right" and input == 2:
        return 20*1.2
    elif button_name == "do_pause" and input == 3:
        return 20*1.2
    elif button_name == "difficulty" and input == 4:
        return 20*1.2
    else: 
        return 20
    