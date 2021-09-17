from imports import *
from hover_button import HoverButton
from switch_button import SwitchButton
from custom_spinner import CustomSpinner

Builder.load_file("game_settings_window.kv")


class GameSettingsWindow(Widget):
    def __init__(self, *args, **kwargs):
        super(GameSettingsWindow, self).__init__(*args, **kwargs)
        self.player_icons = dict()
        self.enemy_icons = dict()

        # Icon displays
        self.display_player = None
        self.display_enemy = None

        self.icons = {
            "player_1": "graphics/icons/circle_place.png",
            "player_2": "graphics/icons/cross_place.png",
            "player_3": "graphics/icons/triangle_place.png",
            "player_4": "graphics/icons/beer_place.png",
            "player_5": "graphics/icons/vodka_place.png",
            "player_6": "graphics/icons/wine_place.png",
            "player_7": "graphics/icons/dog_place.png",
            "player_8": "graphics/icons/cat_place.png",
            "player_9": "graphics/icons/pigeon_place.png",
            "enemy_1": "graphics/icons/circle_place.png",
            "enemy_2": "graphics/icons/cross_place.png",
            "enemy_3": "graphics/icons/triangle_place.png",
            "enemy_4": "graphics/icons/beer_place.png",
            "enemy_5": "graphics/icons/vodka_place.png",
            "enemy_6": "graphics/icons/wine_place.png",
            "enemy_7": "graphics/icons/dog_place.png",
            "enemy_8": "graphics/icons/cat_place.png",
            "enemy_9": "graphics/icons/pigeon_place.png"
        }

        self.displays = {
            "player_1": "graphics/icons/circle_icon_display.png",
            "player_2": "graphics/icons/cross_icon_display.png",
            "player_3": "graphics/icons/triangle_icon_display.png",
            "player_4": "graphics/icons/beer_icon_display.png",
            "player_5": "graphics/icons/vodka_icon_display.png",
            "player_6": "graphics/icons/wine_icon_display.png",
            "player_7": "graphics/icons/dog_icon_display.png",
            "player_8": "graphics/icons/cat_icon_display.png",
            "player_9": "graphics/icons/pigeon_icon_display.png",
            "enemy_1": "graphics/icons/circle_icon_display.png",
            "enemy_2": "graphics/icons/cross_icon_display.png",
            "enemy_3": "graphics/icons/triangle_icon_display.png",
            "enemy_4": "graphics/icons/beer_icon_display.png",
            "enemy_5": "graphics/icons/vodka_icon_display.png",
            "enemy_6": "graphics/icons/wine_icon_display.png",
            "enemy_7": "graphics/icons/dog_icon_display.png",
            "enemy_8": "graphics/icons/cat_icon_display.png",
            "enemy_9": "graphics/icons/pigeon_icon_display.png"
        }

    def create_references(self):
        # Icon displays references
        self.display_player = self.ids["display_player"].__self__
        self.display_enemy = self.ids["display_enemy"].__self__

        # All icon pickers references
        for i in self.ids:
            if i[0] == "p":
                self.player_icons[i] = self.ids[i].__self__
            elif i[0] == "e":
                self.enemy_icons[i] = self.ids[i].__self__

        # Starting conditions
        self.player_icons["player_1"].switch()
        self.player_icons["player_1"].disabled = True
        self.display_player.source = self.displays["player_1"]

        self.enemy_icons["enemy_2"].switch()
        self.enemy_icons["enemy_2"].disabled = True
        self.display_enemy.source = self.displays["enemy_2"]

        self.enemy_icons["enemy_1"].disabled = True
        self.player_icons["player_2"].disabled = True

        if self.enemy_icons["enemy_1"].disabled_image:
            self.enemy_icons["enemy_1"].source = self.enemy_icons["enemy_1"].disabled_image

        if self.player_icons["player_2"].disabled_image:
            self.player_icons["player_2"].source = self.player_icons["player_2"].disabled_image

    def switch_rest(self, icon_name):
        icons_self = None
        icons_enemy = None

        if icon_name[:6] == "player":
            icons_self = self.player_icons
            icons_enemy = self.enemy_icons
        elif icon_name[:5] == "enemy":
            icons_self = self.enemy_icons
            icons_enemy = self.player_icons

        for i, j in zip(icons_self, icons_enemy):
            if i == icon_name:
                icons_enemy[j].disabled = True
                icons_self[i].disabled = True
                if icons_enemy[j].disabled_image:
                    icons_enemy[j].source = icons_enemy[j].disabled_image
            elif icons_enemy[j].source == icons_enemy[j].switch_image:
                pass
            else:
                icons_self[i].source = icons_self[i].normal_image
                icons_self[i].switched = False
                icons_enemy[j].source = icons_enemy[j].normal_image
                icons_enemy[j].switched = False
                icons_enemy[j].disabled = False
                icons_self[i].disabled = False
