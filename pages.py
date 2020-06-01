import pygame
import os
from pygame.sprite import RenderUpdates
from Player import Player
from UIElement import UIElement, BLUE, WHITE, TextElement
from DatabaseInteract import DatabaseInteract
from Brickbreaker import Brickbreaker
from GameState import GameState
from HighscorePage import highscore, show_top10
from numpy.random import choice

CRNT_PATH = os.path.dirname(__file__)
SOUND_PATH = os.path.join(CRNT_PATH, "soundtrack")
# Music Copyright (C) by Simon Kiefer and Julian Stein
SOUNDFILES = ["brick_breaker_ost_1.wav", "brick_breaker_ost_2.wav"]

MAXIMUM_DIFFICULTY = 4
MINIMUM_DIFFICULTY = 1

GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Pages:

    def title_screen(self, screen):
        """
        description:
            - Title page
        :param screen: actual screen
        :return: result of game_loop
        """
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
        play_music_btn = UIElement(
            center_position=(400, 500),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="♫",
            action=GameState.PLAY_MUSIC,
        )

        buttons = RenderUpdates(start_btn, quit_btn, settings_btn, highscore_btn, play_music_btn)

        return self.game_loop(screen, buttons, 0)

    def play_level(self, screen, player):
        quit_btn = UIElement(
            center_position=(400, 400),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Beenden",
            action=GameState.QUIT,
        )
        buttons = RenderUpdates(quit_btn)

        return self.game_loop(screen, buttons, 1)

    def highscore_page(self, screen, player):
        """
        description:
            - Highscore page
        :param screen: actual screen
        :param player: player object
        :return: result of game_loop
        """        
        font = pygame.font.SysFont("Arial", 16)

        my_score = 4
        show_top10(screen)

        txt_surf = font.render("Ready to continue...", True, WHITE)
        txt_rect = txt_surf.get_rect(center=(400, 300))
        screen.blit(txt_surf, txt_rect)
        pygame.display.flip()
        return GameState.TITLE

    def settings_page(self, screen, player):
        """
        description:
            - Settings page
        :param screen: actual screen
        :param player: player object
        :return: result of game_loop
        """
        # Datenbank zum auslesen der aktuellen Einstellungen
        dbi = DatabaseInteract()
        sets = dbi.get_settings()

        heading = TextElement(
            center_position=(400, 80),
            font_size=25,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Einstellungen",
        )
        return_btn = UIElement(
            center_position=(140, 570),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Zurück zum Hauptmenü",
            action=GameState.TITLE,
        )

        move_left = UIElement(
            center_position=(400, 150),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Nach Links: {sets[1]}",
            action=GameState.SETTINGS_HIGHLITED_MOVE_LEFT,
        ) 

        move_right = UIElement(
            center_position=(400, 200),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Nach Rechts: {sets[3]}",
            action=GameState.SETTINGS_HIGHLITED_MOVE_RIGHT,
        )     

        shoot_ball = UIElement(
            center_position=(400, 250),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Ball schiessen: {sets[8]}",
            action=GameState.SETTINGS_HIGHLITED_SHOOT_BALL,
        )  

        do_pause = UIElement(
            center_position=(400, 300),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Pausenmenü: {sets[5]}",
            action=GameState.SETTINGS_HIGHLITED_DO_PAUSE,
        )    

        difficulty = UIElement(
            center_position=(400, 350),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Schwierigkeit: {sets[7]}",
            action=GameState.SETTINGS_HIGHLITED_DIFFICULTY,
        )     

        buttons = RenderUpdates(return_btn, move_left, move_right, do_pause, difficulty, heading, shoot_ball)

        return self.game_loop(screen, buttons, 0)

    def settings_page_highlited(self, screen, player, highlited_btn):
        """
        description:
            - Settings page
        :param screen: actual screen
        :param player: player object
        :param highlited_btn: selected button 
        :return: result of game_loop
        """
        # Datenbank zum auslesen der aktuellen Einstellungen
        # ansicht der Settings seite zum Auswaehlen des Buttons L/R/Pause 
        dbi = DatabaseInteract()
        sets = dbi.get_settings()

        heading = TextElement(
            center_position=(400, 80),
            font_size=25,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Einstellungen",
        )
        return_btn = UIElement(
            center_position=(140, 570),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Zurück zum Hauptmenü",
            action=GameState.TITLE,
        )

        move_left = TextElement(
            center_position=(400, 150),
            font_size=font_size_picker("move_left", highlited_btn),
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Nach Links: {sets[1]}",
        ) 

        move_right = TextElement(
            center_position=(400, 200),
            font_size=font_size_picker("move_right", highlited_btn),
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Nach Rechts: {sets[3]}",
        )     

        shoot_ball = TextElement(
            center_position=(400, 250),
            font_size=font_size_picker("shoot_ball", highlited_btn),
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Ball schiessen: {sets[8]}",
        )  

        do_pause = TextElement(
            center_position=(400, 300),
            font_size=font_size_picker("do_pause", highlited_btn),
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=f"Pausenmenü: {sets[5]}",
        )    

        if highlited_btn !=4 :
            difficulty = TextElement(
                center_position=(400, 350),
                font_size=font_size_picker("difficulty", highlited_btn),
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text=f"Schwierigkeit: {sets[7]}",
            )
        else:
            difficulty = TextElement(
                center_position=(400, 350),
                font_size=font_size_picker("difficulty", highlited_btn),
                bg_rgb=BLUE,
                text_rgb=WHITE,
                text=f"Schwierigkeit: {sets[7]} (mit '+' und '-' anpassen max. 4 min. 1)",
            )

        buttons = RenderUpdates(return_btn, move_left, move_right, do_pause, difficulty, heading, shoot_ball)

        return self.game_loop(screen, buttons, highlited_btn * -1)

    def game_loop(self,screen, buttons, level):
        """ Handles game loop until an action is return by a button in the
            buttons sprite renderer.
        """
        dbi = DatabaseInteract()
        sets = dbi.get_settings()

        play_music = sets[10] == 1
        if play_music:
            track_path = os.path.join(SOUND_PATH, choice(SOUNDFILES, 1, p=[0.5, 0.5])[0])
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

        while True:

            mouse_up = False

            if level < 0:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return GameState.SETTINGS         

                        if level == -1:
                            if event.key != int(sets[4]) and event.key != int(sets[6]) and event.key != int(sets[9]):
                                if event.key == pygame.K_LEFT:
                                    dbi.update_move_left("<-", event.key)
                                elif event.key == pygame.K_RIGHT:
                                    dbi.update_move_left("->", event.key)
                                else:
                                    dbi.update_move_left(event.unicode, event.key)

                        elif level == -2:
                            if event.key != int(sets[2]) and event.key != int(sets[6]) and event.key != int(sets[9]):
                                if event.key == pygame.K_LEFT:
                                    dbi.update_move_right("<-", event.key)
                                elif event.key == pygame.K_RIGHT:
                                    dbi.update_move_right("->", event.key)
                                else:
                                    dbi.update_move_right(event.unicode, event.key)

                        elif level == -3:
                            if event.key != int(sets[2]) and event.key != int(sets[4]) and event.key != int(sets[9]):
                                dbi.update_do_pause(event.unicode, event.key)

                        elif level == -4:
                            # Change keys depending on OS; this version works for MacOS
                            # Windows: K_PLUS --> 93, K_KP_PLUS --> 270
                            if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                                if sets[7] < MAXIMUM_DIFFICULTY:
                                    dbi.update_difficulty(sets[7] + 1)
                            # Windows: K_MINUS --> 47, K_KP_MINUS --> 269
                            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                                if sets[7] > MINIMUM_DIFFICULTY:
                                    dbi.update_difficulty(sets[7] - 1)

                        elif level == -5:
                            if event.key != int(sets[2]) and event.key != int(sets[4]) and event.key != int(sets[6]):
                                if event.key == pygame.K_SPACE:
                                    dbi.update_shoot_button('Leertaste', event.key)
                                else:
                                    dbi.update_shoot_button(event.unicode, event.key)

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
                return Brickbreaker().main()

            pygame.display.flip()

    def game_state_logic(self, game_state, screen, player):
        """
        description:
            - Switch between different pages
        :param screen: the screen to draw the images on
        :param game_state: next page to be shown
        :param player: the player object 
        :return: next GameState
        """
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

        if game_state == GameState.SETTINGS_HIGHLITED_SHOOT_BALL:
            game_state = self.settings_page_highlited(screen, player, 5)

        if game_state == GameState.QUIT:
            game_state = GameState.QUIT

        if game_state == GameState.PLAY_MUSIC:
            dbi = DatabaseInteract()
            if pygame.mixer.music.get_busy():
                dbi.update_play_music(0)
            else:
                dbi.update_play_music(1)
            game_state = self.title_screen(screen)

        return game_state  


def font_size_picker(button_name, input):
    """
    description:
        - Increase font for highlited button
    :param buttonname: the button to be determined wheter to be bigger or not
    :param game_state: the button to be highlighted
    :return: int font size
    """
    if button_name == "move_left" and input == 1:
        return 20*1.2
    elif button_name == "move_right" and input == 2:
        return 20*1.2
    elif button_name == "do_pause" and input == 3:
        return 20*1.2
    elif button_name == "difficulty" and input == 4:
        return 20*1.2
    elif button_name == "shoot_ball" and input == 5:
        return 20*1.2
    else: 
        return 20
