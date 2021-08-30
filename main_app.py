from imports import *
from game_window import GameWindow
from menu_window import MenuWindow
from game_settings_window import GameSettingsWindow
from app_settings_window import AppSettingsWindow
from game_template import Game, Segment

Builder.load_file("main_app.kv")

# TODO: MAKE THE GAME PLAYABLE
"""
Implement TicTacToe_AI
Make segment highlight
Make visualisation for segment choosing method
Change segment color when finished
Make the game winnable
Add AI levels (random, depth=0, depth=3)
"""


# TODO: create own spinner
# TODO: Finish game log
# TODO: Return to the main menu alert popup
# TODO: Icon placing animations
# TODO: Make Instant Place button do something

class MenuScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)


class GameScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(GameScreen, self).__init__(*args, **kwargs)

        self.game_window = None

    def create_references(self):
        self.game_window = self.ids["game_window"].__self__
        self.game_window.create_references()


class GameSettingsScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(GameSettingsScreen, self).__init__(*args, **kwargs)

        self.game_settings_window = None

    def create_references(self):
        self.game_settings_window = self.ids["game_settings_window"].__self__
        self.game_settings_window.create_references()


class AppSettingsScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(AppSettingsScreen, self).__init__(*args, **kwargs)


class GameManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(GameManager, self).__init__(*args, **kwargs)
        self.transition = CardTransition()

        # Creating all app references
        self.menu_screen = self.ids["menu_screen"].__self__
        self.game_screen = self.ids["game_screen"].__self__
        self.game_settings_screen = self.ids["game_settings_screen"].__self__
        self.app_settings_screen = self.ids["app_settings_screen"].__self__

        # Game info
        self.player_sign = None
        self.enemy_sign = None
        self.current_sign = None

        # Game engine
        self.game_engine = Game()
        self.game_engine.player_sign = "X"
        self.game_engine.enemy_sign = "O"
        # TODO: DELETE THIS
        self.game_engine.current_segment = "5"

        # Creating app elements references
        self.create_references()

    def create_references(self):
        self.game_screen.create_references()
        self.game_settings_screen.create_references()

        self.game_settings_screen = self.game_settings_screen.game_settings_window
        self.game_screen = self.game_screen.game_window

        # Game info
        self.player_sign = self.game_settings_screen.icons["player_1"]
        self.enemy_sign = self.game_settings_screen.icons["enemy_2"]
        self.current_sign = self.player_sign

    def set_player_sign(self, sign_name):
        player_data = self.game_settings_screen.display_player, self.game_settings_screen.player_icons
        enemy_data = self.game_settings_screen.display_enemy, self.game_settings_screen.enemy_icons
        display, icons = player_data if sign_name[0] == "p" else enemy_data

        # Changing icon on display
        display.source = icons[sign_name].normal_image

        # Changing gaming icon
        if sign_name[0] == "p":
            self.player_sign = self.game_settings_screen.icons[sign_name]
        elif sign_name[0] == "e":
            self.enemy_sign = self.game_settings_screen.icons[sign_name]

        ####################################
        self.current_sign = self.player_sign

    def restart_game_engine(self):
        self.game_engine.game_map.segments = {str(i): Segment(str(i)) for i in range(1, 10)}
        # TODO: DELETE THIS
        self.game_engine.current_segment = "5"

    def next_turn(self, place_number):
        # Player turn
        self.game_screen.place_sign(self.game_engine.current_segment, place_number, self.player_sign)
        self.game_engine.place_sign(self.game_engine.current_segment, place_number, self.game_engine.player_sign)

        self.game_screen.disable_segments()
        self.game_engine.game_map.update()
        self.game_screen.game_map.segments[self.game_engine.current_segment].places[place_number].if_disabled = True

        self.game_engine.game_map.print()
        print(self.game_engine.current_segment, place_number)

        self.game_engine.current_segment = place_number

        # Enemy turn
        Clock.schedule_once(lambda a: self.enemy_turn(), 2)

    def enemy_turn(self):
        enemy_place_number = self.game_engine.ai_pick_place_number()

        self.game_screen.place_sign(self.game_engine.current_segment, enemy_place_number, self.enemy_sign)
        self.game_engine.place_sign(self.game_engine.current_segment, enemy_place_number, self.game_engine.enemy_sign)

        self.game_screen.game_map.segments[self.game_engine.current_segment].places[enemy_place_number].on_click()
        self.game_engine.game_map.update()
        self.game_screen.game_map.segments[self.game_engine.current_segment].places[enemy_place_number].if_disabled = True

        self.game_engine.game_map.print()
        print(self.game_engine.current_segment, enemy_place_number)

        self.game_engine.current_segment = enemy_place_number
        self.game_screen.activate_segment(enemy_place_number)
