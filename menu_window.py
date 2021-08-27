from imports import *
from hover_button import HoverButton

Builder.load_file("menu_window.kv")
val = 50
Window.size = 10 * val, 16 * val


class MenuWindow(Widget):
    def __init__(self, *args, **kwargs):
        super(MenuWindow, self).__init__(*args, **kwargs)
