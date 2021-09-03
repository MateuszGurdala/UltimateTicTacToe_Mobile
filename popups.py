from imports import *

Builder.load_file("popups.kv")


class ReturnPopup(Popup):
    def __init__(self, *args, **kwargs):
        super(ReturnPopup, self).__init__(*args, **kwargs)



class WinnerPopup(Popup):
    def __init__(self, *args, **kwargs):
        super(WinnerPopup, self).__init__(*args, **kwargs)
