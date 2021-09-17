from imports import *
from switch_button import SwitchButton

Builder.load_file("custom_spinner.kv")


class CustomSpinner(Widget):
    def __init__(self, *args, **kwargs):
        super(CustomSpinner, self).__init__(*args, **kwargs)
        self.option_3 = None
        self.option_2 = None
        self.option_1 = None
        self.option_0 = None
        self.base_button = None

        self.bases_normal = {
            "option_0": "graphics/game_mode_spinner/base0_normal.png",
            "option_1": "graphics/game_mode_spinner/base1_normal.png",
            "option_2": "graphics/game_mode_spinner/base2_normal.png",
            "option_3": "graphics/game_mode_spinner/base3_normal.png"
        }
        self.bases_pressed = {
            "graphics/game_mode_spinner/base0_normal.png": "graphics/game_mode_spinner/base0_pressed.png",
            "graphics/game_mode_spinner/base1_normal.png": "graphics/game_mode_spinner/base1_pressed.png",
            "graphics/game_mode_spinner/base2_normal.png": "graphics/game_mode_spinner/base2_pressed.png",
            "graphics/game_mode_spinner/base3_normal.png": "graphics/game_mode_spinner/base3_pressed.png"
        }

        self.duration = 0.2

        Clock.schedule_once(lambda a: self.create_references(), 0.1)

    def create_references(self):
        self.option_3 = self.ids["option_3"].__self__
        self.option_2 = self.ids["option_2"].__self__
        self.option_1 = self.ids["option_1"].__self__
        self.option_0 = self.ids["option_0"].__self__
        self.base_button = self.ids["base_button"].__self__

    def unfold_options(self):
        Animation(pos_hint={"x": 0, "y": -0.81}, duration=self.duration).start(self.option_0)
        Animation(pos_hint={"x": 0, "y": -1.62}, duration=self.duration).start(self.option_1)
        Animation(pos_hint={"x": 0, "y": -2.43}, duration=self.duration).start(self.option_2)
        Animation(pos_hint={"x": 0, "y": -3.24}, duration=self.duration).start(self.option_3)

    def roll_options_up(self):
        Animation(pos_hint={"x": 0, "y": 0.1}, duration=self.duration).start(self.option_0)
        Animation(pos_hint={"x": 0, "y": 0.1}, duration=self.duration).start(self.option_1)
        Animation(pos_hint={"x": 0, "y": 0.1}, duration=self.duration).start(self.option_2)
        Animation(pos_hint={"x": 0, "y": 0.1}, duration=self.duration).start(self.option_3)

    def change_game_mode(self, child):
        self.base_button.source = self.bases_normal[child.text]
        self.base_button.normal_image = self.bases_normal[child.text]
        self.base_button.switch_image = self.bases_pressed[self.base_button.normal_image]
        self.base_button.disabled_image = self.base_button.normal_image

