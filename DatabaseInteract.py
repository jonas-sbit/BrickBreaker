"""
This files handles all database transactions.
"""

import sqlite3
import pygame


class DatabaseInteract:

    def __init__(self):
        self.connection = sqlite3.connect('brickbreaker.db')
        self.cursor = self.connection.cursor()

        # Tabelle fuer Settings anlegen
        createSettings = "CREATE TABLE IF NOT EXISTS settings(setting_id INTEGER PRIMARY KEY, left_button TEXT, left_value TEXT, right_button TEXT, right_value TEXT, pause_button TEXT, pause_value TEXT, difficulty INTEGER, shoot_button TEXT, shoot_value TEXT, play_music INTEGER)"
        self.cursor.execute(createSettings)
        
        # Tabelle fuer scores anlegen
        createHighscores = "CREATE TABLE IF NOT EXISTS highscores(score_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score INTEGER, level INTEGER)"
        self.cursor.execute(createHighscores)

        # Tabelle fuer active games anlegen
        createActiveGame = "CREATE TABLE IF NOT EXISTS activeGames(game_id INTEGER PRIMARY KEY, score INTEGER, level INTEGER)"
        self.cursor.execute(createActiveGame)

        # default value fuer settings ueberschreibt nicht
        self.cursor.execute(f"INSERT OR IGNORE INTO settings VALUES(1, 'a', '97', 'd', '100', 'p', '112', 4, 'Space', '{pygame.K_SPACE}', 1)")
        
        # default value for highscores
        self.cursor.execute("INSERT OR IGNORE INTO highscores VALUES(1, 'Max Mustermann', 0, 0)")

        # default value fuer activeGames ueberschreibt nicht
        self.cursor.execute("INSERT OR IGNORE INTO activeGames VALUES(1, 0, 0)")

        self.connection.commit()

    def get_settings(self):
        self.cursor.execute("SELECT * FROM settings WHERE setting_id = 1")

        return self.cursor.fetchone()

    def update_play_music(self, play_music):
        self.cursor.execute(f"UPDATE settings SET play_music = '{play_music}' WHERE setting_id = 1")

        self.connection.commit()
        
    def update_settings(self, left_button, right_button, pause_button, difficulty):
        self.cursor.execute(f"UPDATE settings SET left_button = '{left_button}',right_button = '{right_button}', pause_button = '{pause_button}', difficulty = {difficulty} WHERE setting_id = 1")

        self.connection.commit()

    def update_shoot_button(self, button, value):
        self.cursor.execute(f"UPDATE settings SET shoot_button = '{button}', shoot_value = '{value}' WHERE setting_id = 1")

        self.connection.commit()


    def update_move_left(self, left_button, left_value):
        self.cursor.execute(f"UPDATE settings SET left_button = '{left_button}', left_value = '{left_value}' WHERE setting_id = 1")

        self.connection.commit()

    def update_move_right(self, right_button, right_value):
        self.cursor.execute(f"UPDATE settings SET right_button = '{right_button}', right_value = '{right_value}' WHERE setting_id = 1")

        self.connection.commit()

    def update_do_pause(self, pause_button, pause_value):
        self.cursor.execute(f"UPDATE settings SET pause_button = '{pause_button}', pause_value = '{pause_value}' WHERE setting_id = 1")

        self.connection.commit()    

    def update_difficulty(self, difficulty):
        self.cursor.execute(f"UPDATE settings SET difficulty = '{difficulty}' WHERE setting_id = 1")

        self.connection.commit()

    def get_scores(self):
        self.cursor.execute("SELECT * FROM highscores")

        return self.cursor.fetchall()

    def insert_score(self, name, score, level):
        self.cursor.execute(f"INSERT INTO highscores (name, score, level) VALUES('{name}', {score}, {level})")

        self.connection.commit()


    def delete_score(self, score_id):
        self.cursor.execute(f"DELETE FROM highscores WHERE score_id = {score_id}")

        self.connection.commit()


    def clear_scores(self):
        self.cursor.execute("DELETE FROM highscores")

        self.connection.commit()

    def get_active_game(self):
        self.cursor.execute("SELECT * FROM activeGames WHERE game_id = 1")

        return self.cursor.fetchone()

    def update_activ_game(self, score, level):
        self.cursor.execute(f"UPDATE activeGames SET score = {score}, level = {level} WHERE game_id = 1")

        self.connection.commit()

    def clear_active_game(self):
        self.cursor.execute("UPDATE activeGames SET score = 0, level = 0 WHERE game_id = 1")

        self.connection.commit()   