import copy

from imports import *
from game_window import GameWindow
from menu_window import MenuWindow
from game_settings_window import GameSettingsWindow
from app_settings_window import AppSettingsWindow
from game_template import Game, Segment

Builder.load_file("main_app.kv")

# TODO: MAKE THE GAME PLAYABLE
"""
Make the game winnable
"""


# TODO: Add AI levels (random, depth=0, depth=3)
# TODO: create own spinner
# TODO: Finish game log
# TODO: Return to the main menu alert popup
# TODO: Icon placing animations
# TODO: Make Instant Place button do something
# TODO: Upgrade Graphics
# TODO: Add clock to create_reference functions inside classes
# TODO: Change function that calls enemy move (enemy_place_number might not be yet evaluated when it is called)

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
        self.game_map = None
        self.game_settings_screen = self.ids["game_settings_screen"].__self__
        self.app_settings_screen = self.ids["app_settings_screen"].__self__

        # Game info
        self.player_sign = None
        self.enemy_sign = None

        # Game engine
        self.game_engine = Game()
        self.game_engine.player_sign = "X"
        self.game_engine.enemy_sign = "O"

        # Creating app elements references
        self.create_references()

    def create_references(self):
        self.game_screen.create_references()
        self.game_settings_screen.create_references()

        self.game_settings_screen = self.game_settings_screen.game_settings_window
        self.game_screen = self.game_screen.game_window
        self.game_map = self.game_screen.ids["game_map"].__self__

        # Game info
        self.player_sign = self.game_settings_screen.icons["player_1"]
        self.enemy_sign = self.game_settings_screen.icons["enemy_2"]

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

    def restart(self):
        # Erasing game engine data
        self.game_engine.game_map.segments = {str(i): Segment(str(i)) for i in range(1, 10)}

        # Restarting GUI
        self.game_screen.hide_segments()
        self.game_screen.remove_highlight()
        self.game_screen.reset_game_map()
        self.game_screen.remove_choose_segment_buttons()

    def next_turn(self, place_number):
        self.update_game(place_number, enemy=False)
        self.game_map.disable_segments()

        if self.game_engine.game_map.segments[place_number].winner:
            print("Segment finished.")
            self.enemy_choose_segment()

            enemy_place_number = self.game_engine.ai_pick_place_number()
            self.enemy_turn_delay(enemy_place_number, 2.5)

        else:
            self.game_engine.current_segment = place_number
            self.game_screen.highlight_segment(place_number)

            enemy_place_number = self.game_engine.ai_pick_place_number()
            self.enemy_turn_delay(enemy_place_number, 1.5)

    def enemy_turn_delay(self, enemy_place_number, delay):
        segment = self.game_map.segments[self.game_engine.current_segment]
        Clock.schedule_once(lambda a: segment.places[enemy_place_number].press(), delay)
        Clock.schedule_once(lambda a: self.enemy_turn(enemy_place_number), delay + 0.5)

    def enemy_turn(self, enemy_place_number):
        self.update_game(enemy_place_number, enemy=True)
        self.game_map.segments[self.game_engine.current_segment].places[enemy_place_number].release()

        if self.game_engine.game_map.segments[enemy_place_number].winner:
            print("Segment finished.")
            self.player_choose_segment()
        else:
            self.game_engine.current_segment = enemy_place_number
            self.game_map.activate_segment(enemy_place_number)
            self.game_screen.highlight_segment(enemy_place_number)

    def update_game(self, place_number, enemy):
        sign = self.enemy_sign if enemy else self.player_sign
        game_engine_sign = self.game_engine.enemy_sign if enemy else self.game_engine.player_sign
        self.game_screen.place_sign(self.game_engine.current_segment, place_number, sign)
        self.game_engine.place_sign(self.game_engine.current_segment, place_number, game_engine_sign)

        self.game_map.segments[self.game_engine.current_segment].places[place_number].release()
        self.game_screen.remove_highlight()
        self.game_engine.game_map.update()
        if self.game_engine.game_map.update():
            self.game_won()
            return
        self.game_screen.update_segment_highlight(self.game_engine.game_map)
        self.game_map.segments[self.game_engine.current_segment].places[place_number].if_disabled = True

        self.game_engine.game_map.print()
        print(f"Segment: {self.game_engine.current_segment} | Place: {place_number}")

    def set_current_segment(self, segment_number):
        self.game_engine.current_segment = segment_number
        self.game_screen.remove_choose_segment_buttons()
        self.game_screen.highlight_segment(segment_number)
        self.game_map.activate_segment(segment_number)
        print(f"Player chose segment: {segment_number}")

    def player_choose_segment(self):
        self.game_map.disable_segments()
        self.game_screen.remove_highlight()
        self.game_screen.create_choose_segment_buttons()

    def enemy_choose_segment(self):
        self.game_engine.current_segment = self.game_engine.ai.choose_segment(self.game_engine.game_map)[0]
        print(f"Enemy chose segment: {self.game_engine.current_segment}")
        self.game_map.disable_segments()
        self.game_screen.remove_highlight()
        self.game_screen.create_choose_segment_buttons(if_disabled=True)

        Clock.schedule_once(lambda a: self.game_screen.remove_choose_segment_buttons(), 2)
        Clock.schedule_once(lambda a: self.game_screen.highlight_segment(self.game_engine.current_segment), 2)

    def game_won(self):
        self.game_map.disable_segments()
        self.game_screen.remove_highlight()
