from imports import *

Builder.load_file("app_settings_window.kv")


class AppSettingsWindow(Widget):
    def __init__(self, *args, **kwargs):
        super(AppSettingsWindow, self).__init__(*args, **kwargs)