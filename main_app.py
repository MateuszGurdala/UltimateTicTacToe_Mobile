import copy
from imports import *
from game_window import GameWindow
from menu_window import MenuWindow
from game_settings_window import GameSettingsWindow
from app_settings_window import AppSettingsWindow
from game_template import Game, Segment
from popups import WinnerPopup

Builder.load_file("main_app.kv")


# TODO: Optimise game log animations
# TODO: Add a draw who starts
# TODO: Icon placement animations
# TODO: Add clock to create_reference functions inside classes
# TODO: Change function that calls enemy move (enemy_place_number might not yet be evaluated when it is called)

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
        self.game_log = None
        self.game_settings_screen = self.ids["game_settings_screen"].__self__
        self.app_settings_screen = self.ids["app_settings_screen"].__self__

        # Game info
        self.game_mode = "ai_normal"
        self.player_sign = None
        self.enemy_sign = None
        self.instant_place = False
        self.enemy_player = False

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
        self.game_screen.root = self
        self.game_map = self.game_screen.ids["game_map"].__self__
        self.game_log = self.game_screen.ids["game_log"].__self__

        # Game info
        self.player_sign = self.game_settings_screen.icons["player_1"]
        self.enemy_sign = self.game_settings_screen.icons["enemy_2"]

    def set_player_sign(self, sign_name):
        player_data = self.game_settings_screen.display_player, self.game_settings_screen.player_icons
        enemy_data = self.game_settings_screen.display_enemy, self.game_settings_screen.enemy_icons
        display, icons = player_data if sign_name[0] == "p" else enemy_data
        displays = self.game_settings_screen.displays
        # Changing icon on display
        display.source = displays[sign_name]

        # Changing gaming icon
        if sign_name[0] == "p":
            self.player_sign = self.game_settings_screen.icons[sign_name]
        elif sign_name[0] == "e":
            self.enemy_sign = self.game_settings_screen.icons[sign_name]

    def change_game_mode(self, game_mode):
        self.game_mode = game_mode

    def add_letter_to_log(self, letter, delay=None):
        if delay:
            Clock.schedule_once(lambda a: self.add_letter_to_log(letter), delay)
            return
        self.game_log.text += letter

    def add_to_log(self, message):
        # n = -1
        # delay = 0.01
        # for i in message:
        #     n += 1
        #     self.add_letter_to_log(message[n], delay)
        #     delay += 0.01
        # self.add_letter_to_log("\n", delay)
        self.game_log.text += message + "\n"

    def restart(self):
        # Erasing game engine data
        self.game_engine.game_map.segments = {str(i): Segment(str(i)) for i in range(1, 10)}

        # Restarting GUI
        self.game_screen.hide_segments()
        self.game_screen.remove_highlight()
        self.game_screen.remove_segment_winner_highlight()
        self.game_screen.reset_game_map()
        self.game_screen.remove_choose_segment_buttons()
        self.game_screen.current_player_display.source = "graphics/game_screen/extend_normal.png"
        self.game_log.text = ""

    def next_turn(self, place_number):
        if not self.instant_place:
            self.game_map.un_click_rest_buttons(self.game_engine.current_segment, place_number)
            place = self.game_map.segments[self.game_engine.current_segment].places[place_number]
            if place.clicked:
                pass
            else:
                place.source = "graphics/game_map/place_highlight.png"
                place.clicked = True
                return

        self.add_to_log(f"Put sign in segment {self.game_engine.current_segment} in place {place_number}")
        if self.enemy_player:
            self.update_game(place_number, enemy=True)
        else:
            self.update_game(place_number, enemy=False)
        if self.game_engine.game_map.winner:
            return
        self.game_map.disable_segments()
        if self.enemy_player:
            self.game_screen.current_player_display.source = self.game_settings_screen.display_player.source
        else:
            self.game_screen.current_player_display.source = self.game_settings_screen.display_enemy.source

        if self.game_engine.game_map.segments[place_number].winner:
            print("Segment finished.")
            self.add_to_log("Moved enemy to a finished segment")
            if self.game_mode != "player_controlled":
                self.enemy_choose_segment()

                enemy_place_number = self.game_engine.ai_pick_place_number("ai_easy")
                self.enemy_turn_delay(enemy_place_number, 2.5)
            else:
                self.player_choose_segment()

                if self.enemy_player:
                    self.enemy_player = False
                else:
                    self.enemy_player = True
        else:
            self.game_engine.current_segment = place_number
            self.game_screen.highlight_segment(place_number)

            if self.game_mode != "player_controlled":
                enemy_place_number = self.game_engine.ai_pick_place_number(self.game_mode)
                self.enemy_turn_delay(enemy_place_number, 1.5)
            else:
                self.game_engine.current_segment = place_number
                self.game_map.activate_segment(place_number)
                self.game_screen.highlight_segment(place_number)
                if self.enemy_player:
                    self.enemy_player = False
                else:
                    self.enemy_player = True

    def enemy_turn_delay(self, enemy_place_number, delay):
        segment = self.game_map.segments[self.game_engine.current_segment]
        Clock.schedule_once(lambda a: segment.places[enemy_place_number].press(), delay)
        Clock.schedule_once(lambda a: self.enemy_turn(enemy_place_number), delay + 0.5)

    def enemy_turn(self, enemy_place_number):
        self.add_to_log(f"Enemy put sign in segment {self.game_engine.current_segment} in place {enemy_place_number}")
        self.update_game(enemy_place_number, enemy=True)
        if self.game_engine.game_map.winner:
            return
        self.game_map.segments[self.game_engine.current_segment].places[enemy_place_number].release()
        self.game_screen.current_player_display.source = self.game_settings_screen.display_player.source

        if self.game_engine.game_map.segments[enemy_place_number].winner:
            print("Segment finished.")
            self.add_to_log("Enemy moved you to a finished segment")
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
        self.game_screen.update_segment_highlight(self.game_engine.game_map)
        if self.game_engine.game_map.winner:
            self.game_won()
            return
        self.game_map.segments[self.game_engine.current_segment].places[place_number].if_disabled = True

        self.game_engine.game_map.print()
        print(f"Segment: {self.game_engine.current_segment} | Place: {place_number}")

    def set_current_segment(self, segment_number):
        self.game_engine.current_segment = segment_number
        self.game_screen.remove_choose_segment_buttons()
        self.game_screen.highlight_segment(segment_number)
        self.game_map.activate_segment(segment_number)
        print(f"Player chose segment: {segment_number}")
        self.add_to_log(f"Chose segment {segment_number}")

    def player_choose_segment(self):
        self.add_to_log("You can choose starting segment")
        self.game_map.disable_segments()
        self.game_screen.remove_highlight()
        self.game_screen.create_choose_segment_buttons()

    def enemy_choose_segment(self):
        self.add_to_log("Enemy is choosing starting segment")
        if self.game_mode in ["ai_hard", "ai_normal"]:
            self.game_engine.current_segment = self.game_engine.ai.choose_segment(self.game_engine.game_map)[0]
        elif self.game_mode == "ai_easy":
            val = randint(1, 9)
            while self.game_engine.game_map.segments[str(val)].winner:
                val = randint(1, 9)
            self.game_engine.current_segment = str(val)
        print(f"Enemy chose segment: {self.game_engine.current_segment}")
        self.add_to_log(f"Enemy chose segment {self.game_engine.current_segment}")
        self.game_map.disable_segments()
        self.game_screen.remove_highlight()
        self.game_screen.create_choose_segment_buttons(if_disabled=True)

        Clock.schedule_once(lambda a: self.game_screen.remove_choose_segment_buttons(), 2)
        Clock.schedule_once(lambda a: self.game_screen.highlight_segment(self.game_engine.current_segment), 2)

    def game_won(self):
        print("Game has been finished.")
        self.add_to_log("Game has been finished")
        winner = "Player" if self.game_engine.game_map.winner == "X" else "Enemy"
        self.add_to_log(f"{winner} has won the game!")
        self.game_map.disable_segments()
        self.game_screen.remove_highlight()
        popup = WinnerPopup(self)
        popup.winner = self.game_engine.game_map.winner
        popup.open()
