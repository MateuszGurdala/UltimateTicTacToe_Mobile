import copy

from imports import *
from place_button import PlaceButton

Builder.load_file("segment.kv")


class Segment(Widget):
    def __init__(self, *args, **kwargs):
        super(Segment, self).__init__(*args, **kwargs)
        self.places = {i: self.ids[i].__self__ for i in self.ids}

