from imports import *

Builder.load_file("place_button.kv")
Window.size = 200, 200


class PlaceButton(ButtonBehavior, Image):
    def __init__(self, *args, **kwargs):
        super(PlaceButton, self).__init__(*args, **kwargs)
        self.number = None
        self.operation = "change_image"
        self.if_disabled = None
        self.clicked = False

        # Images
        self.normal_image = "graphics/game_map/place_normal.png"
        self.hover_image = "graphics/game_map/place_normal.png"
        self.pressed_image = "graphics/game_map/place_normal.png"

    def press(self):
        self.size_hint = 0.8, 0.8

    def release(self):
        self.size_hint = 1, 1

    def pass_function(self, *args):
        pass
