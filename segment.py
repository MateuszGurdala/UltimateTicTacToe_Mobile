import copy

from imports import *
from place_button import PlaceButton

Builder.load_file("segment.kv")
Window.size = 400, 400


class Segment(Widget):
    def __init__(self, *args, **kwargs):
        super(Segment, self).__init__(*args, **kwargs)
        self.places = {i: self.ids[i].__self__ for i in self.ids}


class MainApp(App):
    def __init__(self, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)
        self.title = "Segment"
        self.colors = colors

    @staticmethod
    def build():
        return Segment()


if __name__ == "__main__":
    MainApp().run()
