from imports import *
from game_map import GameMap
from hover_button import HoverButton
from switch_button import SwitchButton
from popups import ReturnPopup

Builder.load_file("game_window.kv")


class GameWindow(Widget):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.root = None

        # References
        self.game_map = None
        self.game_map_layout = None
        self.game_log = None
        self.current_player_display = None

    def create_references(self):
        # Creating Game Map reference
        self.game_map = self.ids["game_map"].__self__
        self.game_map_layout = self.ids["game_map_layout"].__self__
        self.game_log = self.ids["game_log"].__self__
        self.current_player_display = self.ids["current_player_display"].__self__

        # Creating references to all segments and places
        for i in self.game_map.ids:
            self.game_map.segments[i] = self.game_map.ids[i].__self__
            for j in self.game_map.segments[i].ids:
                self.game_map.segments[i].places[j] = self.game_map.segments[i].ids[j].__self__

    def set_display(self):
        self.current_player_display.source = self.parent.parent.game_settings_screen.display_player.source

    def place_sign(self, segment_number, place_number, sign_graphic):
        self.game_map.segments[segment_number].places[place_number].source = sign_graphic

    def reset_game_map(self):
        Clock.schedule_once(lambda a: self.game_map.reset(), 1)

    def discover_segments(self):
        self.root.add_to_log("Creating game map")
        game_modes = {
            "ai_easy": "Easy",
            "ai_normal": "Normal",
            "ai_hard": "Hard",
            "player_controlled": "Player Controlled",
        }
        self.root.add_to_log("Game mode: " + game_modes[self.root.game_mode])
        Clock.schedule_once(lambda a: self.game_map.discover_segments(), 1)
        Clock.schedule_once(lambda a: self.set_display(), 3)
        Clock.schedule_once(lambda a: self.root.add_to_log("You can choose starting segment"), 3)

    def hide_segments(self):
        Clock.schedule_once(lambda a: self.game_map.hide_segments(), 1)

    def highlight_segment(self, segment_number):
        src = "graphics/game_map/current_segment_highlight.png"
        segment = self.game_map.segments[segment_number]
        segment.canvas.before.add(Rectangle(size=segment.size, pos=segment.pos, source=src))

    def remove_highlight(self):
        for i in self.game_map.segments:
            if not self.game_map.segments[i].highlight:
                self.game_map.segments[i].canvas.before.clear()

    def remove_segment_winner_highlight(self):
        for i in self.game_map.segments:
            self.game_map.segments[i].highlight = None
            self.game_map.segments[i].canvas.before.clear()

    def create_choose_segment_buttons(self, if_disabled=False):
        for i in self.game_map.segments:
            if not self.game_map.segments[i].highlight:
                self.game_map.create_choose_button(i, if_disabled)

    def remove_choose_segment_buttons(self):
        for i in self.game_map.segments:
            self.game_map.remove_choose_button(i)

    def update_segment_highlight(self, game_engine_map):
        for i in game_engine_map.segments:
            if game_engine_map.segments[i].winner:
                src = None
                if game_engine_map.segments[i].winner == "X":
                    src = "graphics/game_map/player_segment_highlight.png"
                elif game_engine_map.segments[i].winner == "O":
                    src = "graphics/game_map/enemy_segment_highlight.png"
                self.game_map.segments[i].highlight = src
                segment = self.game_map.segments[i]
                segment.canvas.before.add(Rectangle(size=segment.size, pos=segment.pos, source=src))
