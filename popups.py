from imports import *

Builder.load_file("popups.kv")


class ReturnPopup(Popup):
    def __init__(self, *args, **kwargs):
        super(ReturnPopup, self).__init__(*args, **kwargs)


class WinnerPopup(Popup):
    def __init__(self, parent, *args, **kwargs):
        super(WinnerPopup, self).__init__(*args, **kwargs)
        self.root = parent
        self.winner = None

        Clock.schedule_once(lambda a: self.set_winner_display(), 0.01)

    def set_winner_display(self):
        root = self.root.game_settings_screen
        image = root.display_player.source if self.winner == "X" else root.display_enemy.source
        self.ids["winner_image"].source = image
