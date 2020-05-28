import pygame
from Player import Player
from pages import Pages, GameState

def main():
    pygame.init()

    # Groesse fuer das Fenster festlegen
    screen = pygame.display.set_mode((800, 600))

    # Standardmaessig mit Title Seite anfangen
    game_state = GameState.TITLE
    player = Player()

    # Aufrufen der Logik, die die Pages aufruft
    while True:
        game_state = Pages().game_state_logic(game_state, screen, player)

        if game_state == game_state.QUIT:
            pygame.quit()
            return

if __name__ == "__main__":
    main()