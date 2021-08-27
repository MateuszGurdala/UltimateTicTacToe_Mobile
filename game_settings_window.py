from imports import *
from hover_button import HoverButton
from switch_button import SwitchButton

Builder.load_file("game_settings_window.kv")


class GameSettingsWindow(Widget):
    def __init__(self, *args, **kwargs):
        super(GameSettingsWindow, self).__init__(*args, **kwargs)
        self.player_icons = dict()
        self.enemy_icons = dict()

    def create_references(self):
        n = 1
        for i in self.ids:
            if n < 10:
                self.player_icons[i] = self.ids[i].__self__
            else:
                self.enemy_icons[i] = self.ids[i].__self__
            n += 1
        self.player_icons["player_1"].switch()
        self.enemy_icons["enemy_2"].switch()
        self.player_icons["player_1"].disabled = True
        self.enemy_icons["enemy_2"].disabled = True
        self.enemy_icons["enemy_1"].disabled = True
        self.player_icons["player_2"].disabled = True

    def switch_rest(self, icon_name):
        if icon_name[:6] == "player":
            icons_self = self.player_icons
            icons_enemy = self.enemy_icons
        elif icon_name[:5] == "enemy":
            icons_self = self.enemy_icons
            icons_enemy = self.player_icons

        #TODO: FIX
        for i, j in zip(icons_self, icons_enemy):
            if i == icon_name:
                icons_enemy[j].disabled = True
                icons_self[i].disabled = True
            else:
                icons_self[i].source = icons_self[i].normal_image
                icons_enemy[j].disabled = False
                icons_self[i].disabled = False
