import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates
from pygame.locals import *
from DatabaseInteract import DatabaseInteract
from UIElement import UIElement, WHITE, BLUE
from Player import Player
from pages import Pages, GameState
from Brickbreaker import Brickbreaker
import sys


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()



def main():
    pygame.init()

    screen = pygame.display.set_mode((1000, 750))
    game_state = GameState.TITLE

    player = Player()

    # Aufrufen der Pages
    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = play_level(screen, player)

        if game_state == GameState.NEXT_LEVEL:
            player.current_level += 1
            game_state = play_level(screen, player)

        if game_state == GameState.HIGHSCORE:
            game_state = highscore_page(screen, player)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen):
    return Pages().title_screen(screen)
    
def play_level(screen, player):
    return Pages().play_level(screen, player)

def highscore_page(screen, player):
    return Pages().highscore_page(screen, player)





if __name__ == "__main__":
    main()