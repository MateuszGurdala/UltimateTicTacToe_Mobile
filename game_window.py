from imports import *
from game_map import GameMap
from hover_button import HoverButton
from switch_button import SwitchButton

Builder.load_file("game_window.kv")


class GameWindow(Widget):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)

        # References
        self.game_map = None
        self.game_map_layout = None
        self.game_log_layout = None

        self.log_extended = False

    def create_references(self):
        # Creating Game Map reference
        self.game_map = self.ids["game_map"].__self__
        self.game_log_layout = self.ids["game_log_layout"].__self__
        self.game_map_layout = self.ids["game_map_layout"].__self__

        # Creating references to all segments and places
        for i in self.game_map.ids:
            self.game_map.segments[i] = self.game_map.ids[i].__self__
            for j in self.game_map.segments[i].ids:
                self.game_map.segments[i].places[j] = self.game_map.segments[i].ids[j].__self__

    def extend_game_log(self):
        if not self.log_extended:
            animation.extend_log(self.game_log_layout, self.game_map_layout, 3 / 13)
            self.log_extended = True
        elif self.log_extended:
            animation.hide_log(self.game_log_layout, self.game_map_layout, 12.5 / 13)
            self.log_extended = False

    def discover_segments(self):
        Clock.schedule_once(lambda a: self.game_map.discover_segments(), 1)

    def disable_segments(self):
        self.game_map.disable_segments()

    def activate_segment(self, segment_number):
        self.game_map.activate_segment(segment_number)

    def hide_segments(self):
        Clock.schedule_once(lambda a: self.game_map.hide_segments(), 1)

    def reset_game_map(self):
        Clock.schedule_once(lambda a: self.game_map.reset(), 1)

    def place_sign(self, segment_number, place_number, sign_graphic):
        self.game_map.segments[segment_number].places[place_number].source = sign_graphic
