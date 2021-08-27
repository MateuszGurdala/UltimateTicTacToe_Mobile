from imports import *

Builder.load_file("switch_button.kv")
Window.size = 200, 200


class SwitchButton(ButtonBehavior, Image):
    def __init__(self, *args, **kwargs):
        super(SwitchButton, self).__init__(*args, **kwargs)
        self.name = None

        self.normal = None
        self.press = None

        # Images
        self.normal_image = None
        self.switch_image = None

    # Action methods
    def click(self):
        self.size_hint = self.press

    def switch(self):
        if self.source == self.normal_image:
            self.source = self.switch_image
        elif self.source == self.switch_image:
            self.source = self.normal_image
        self.size_hint = self.normal

    def pass_function(self):
        pass
