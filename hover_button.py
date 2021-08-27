from imports import *

Builder.load_file("hover_button.kv")
Window.size = 200, 200


class HoverButton(ButtonBehavior, Image):
    def __init__(self, *args, **kwargs):
        super(HoverButton, self).__init__(*args, **kwargs)
        self.normal = None
        self.hover = None
        self.press = None

        # Images
        self.normal_image = None
        self.hover_image = None
        self.pressed_image = None

        Window.bind(mouse_pos=self.on_mouse_pos)

    # Hover methods
    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        if self.collide_point(*pos):
            Clock.schedule_once(lambda a: self.on_enter())
        else:
            Clock.schedule_once(lambda a: self.on_leave())

    def on_leave(self, *args):
        self.size_hint = self.normal
        self.source = self.normal_image

    def on_enter(self, *args):
        self.size_hint = self.hover
        self.source = self.hover_image

    # Action methods
    def click(self):
        self.source = self.pressed_image
        self.size_hint = self.press

    def release(self):
        self.source = self.normal_image
        self.size_hint = self.normal

    def pass_function(self):
        pass
