import pygame
from Player import Player
from pages import Pages
from GameState import GameState
# from GameElements import Special, Random_Show_Special

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

def main():
    pygame.init()

    # Groesse fuer das Fenster festlegen
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    # Standardmaessig mit Title Seite anfangen
    game_state = GameState.TITLE
    player = Player()

    # TEST Julian
    #special = Special((100,100))
    #if Random_Show_Special():
    #    special.show_special()


    # Aufrufen der Logik, die die Pages aufruft
    while True:
        game_state = Pages().game_state_logic(game_state, screen, player)

        if game_state == game_state.QUIT:
            pygame.quit()
            return

if __name__ == "__main__":
    main()