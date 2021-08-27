from imports import *
from game_map import GameMap
from hover_button import HoverButton
from switch_button import SwitchButton

Builder.load_file("game_window.kv")


class GameWindow(Widget):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)

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
            Animation(size_hint=(1, 12 / 16), duration=0.2).start(self.game_log_layout)
            Animation(size_hint=(1, 1 / 16), duration=0.2).start(self.game_map_layout)
            self.log_extended = True
        elif self.log_extended:
            Animation(size_hint=(1, 3 / 16), duration=0.2).start(self.game_log_layout)
            Animation(size_hint=(1, 10 / 16), duration=0.2).start(self.game_map_layout)
            self.log_extended = False

    def discover_segments(self):
        Clock.schedule_once(lambda a: self.game_map.discover_segments(), 1)

    def hide_segments(self):
        Clock.schedule_once(lambda a: self.game_map.hide_segments(), 1)
