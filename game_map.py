import copy

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
                Window.unbind(mouse_pos=self.segments[i].places[j].on_mouse_pos)

    def activate_segment(self, segment_number):
        for i in self.segments[segment_number].places:
            if not self.segments[segment_number].places[i].if_disabled:
                self.segments[segment_number].places[i].disabled = False
                Window.bind(mouse_pos=self.segments[segment_number].places[i].on_mouse_pos)

    def create_choose_button(self, segment_number, if_disabled=False):
        segment = self.segments[segment_number]
        # It looks terrible but everything else failed
        root = self.parent.parent.parent.parent.parent
        button = Button(pos=segment.pos,
                        size=segment.size,
                        background_normal="graphics/game_map/choose_segment_button.png",
                        background_down="graphics/game_map/choose_segment_button.png",
                        on_release=lambda a: root.set_current_segment(segment_number),
                        disabled=if_disabled)
        self.segments[segment_number].choose_button = button
        self.segments[segment_number].add_widget(self.segments[segment_number].choose_button)

    def remove_choose_button(self, segment_number):
        segment = self.segments[segment_number]
        if segment.choose_button:
            segment.remove_widget(segment.choose_button)
            segment.choose_button = None
