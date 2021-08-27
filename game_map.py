from imports import *
from segment import Segment

Builder.load_file("game_map.kv")
Window.size = 400, 400


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
                self.segments[i].places[j].size_hint = 0,0

class MainApp(App):
    def __init__(self, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)
        self.title = "Game Map"
        self.colors = colors

    @staticmethod
    def build():
        return GameMap()


if __name__ == "__main__":
    MainApp().run()
