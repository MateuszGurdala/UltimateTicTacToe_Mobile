# TODO: create own spinner
from kivy.config import Config

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 700)
Config.set('graphics', 'top', 100)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'borderless', 'true')

from imports import *
from game_window import GameWindow
from menu_window import MenuWindow
from game_settings_window import GameSettingsWindow
from app_settings_window import AppSettingsWindow

Builder.load_file("main_app.kv")
val = 50
Window.size = 10 * val, 16 * val


class MenuScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)


class GameScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(GameScreen, self).__init__(*args, **kwargs)

    def create_references(self):
        self.game_window = self.ids["game_window"].__self__
        self.game_window.create_references()


class GameSettingsScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(GameSettingsScreen, self).__init__(*args, **kwargs)

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


class MainApp(App):
    def __init__(self, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)
        self.title = "UltimateTicTacToe"
        self.colors = colors

    @staticmethod
    def build():
        return GameManager()


if __name__ == "__main__":
    MainApp().run()
