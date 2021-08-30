from imports import *
from segment import Segment

Builder.load_file("game_map.kv")


class GameMap(FloatLayout):
    def __init__(self, *args, **kwargs):
        super(GameMap, self).__init__(*args, **kwargs)

        # Creating references to all segment objects
        self.segments = {i: self.ids[i].__self__ for i in self.ids}

        # Creating places references for every segment
        for i in self.segments:
            self.segments[i].places = {j: self.segments[i].ids[j].__self__ for j in self.segments[i].ids}

    def discover_segments(self):
        for i in self.segments:
            animation.segment_entrance_animation(self.segments[i])

    def hide_segments(self):
        for i in self.segments:
            for j in self.segments[i].places:
                self.segments[i].places[j].size_hint = 0, 0

    def reset(self):
        for i in self.segments:
            for j in self.segments[i].places:
                self.segments[i].places[j].source = self.segments[i].places[j].normal_image

    def disable_segments(self):
        for i in self.segments:
            for j in self.segments[i].places:
                self.segments[i].places[j].disabled = True

    def activate_segment(self, segment_number):
        for i in self.segments[segment_number].places:
            if not self.segments[segment_number].places[i].if_disabled:
                self.segments[segment_number].places[i].disabled = False
