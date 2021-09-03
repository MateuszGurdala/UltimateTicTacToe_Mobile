from imports import *

Builder.load_file("switch_button.kv")


class SwitchButton(ButtonBehavior, Image):
    def __init__(self, *args, **kwargs):
        super(SwitchButton, self).__init__(*args, **kwargs)
        self.switched = False

        self.normal = None
        self.press = None

        # Images
        self.normal_image = None
        self.switch_image = None
        self.disabled_image = None

    # Action methods
    def click(self):
        self.size_hint = self.press

    def switch(self):
        if self.switched:
            self.source = self.normal_image
            self.switched = False
        else:
            self.source = self.switch_image
            self.switched = True
        self.size_hint = self.normal

    def pass_function(self):
        pass
