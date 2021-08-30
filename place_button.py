from imports import *

Builder.load_file("place_button.kv")
Window.size = 200, 200


class PlaceButton(ButtonBehavior, Image):
    def __init__(self, *args, **kwargs):
        super(PlaceButton, self).__init__(*args, **kwargs)
        self.number = None
        self.operation = "change_image"
        self.if_disabled = None

        # Images
        self.normal_image = "graphics/game_map/place_normal.png"
        self.hover_image = "graphics/game_map/place_normal.png"
        self.pressed_image = "graphics/game_map/place_normal.png"

        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        if self.collide_point(*pos):
            Clock.schedule_once(lambda a: self.on_enter(self.operation))
        else:
            Clock.schedule_once(lambda a: self.on_leave(self.operation))

    def on_leave(self, operation, *args):
        if operation == "change_size":
            self.size_hint = (1, 1)
        elif operation == "change_image":
            self.source = self.normal_image

    def on_enter(self, operation, *args):
        if operation == "change_size":
            self.size_hint = (0.9, 0.9)
        elif operation == "change_image":
            self.source = self.hover_image

    def on_click(self):
        Window.unbind(mouse_pos=self.on_mouse_pos)
        # animation.place_sign_animation(self, 1, animation.cross_animation)

    def pass_function(self, *args):
        pass
