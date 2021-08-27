from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, StringProperty
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Canvas, Color
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.animation import Animation

from animation import animation

colors = {
    "light_blue": get_color_from_hex("#a1d1cc"),
    "dark_blue": get_color_from_hex("#2ea699"),
    "green": get_color_from_hex("#23e615"),
    "dark_green": get_color_from_hex("#49ba1f"),
    "dark_grey": get_color_from_hex("#1b1c1b"),
    "light_grey": get_color_from_hex("#8d8d8d"),
    "orange": get_color_from_hex("#ff8308"),
    "white": get_color_from_hex("#cccccc"),
    "grey": get_color_from_hex("#7e8282"),
    "red": get_color_from_hex("#e41d1d"),
    "light_red": get_color_from_hex("#ff7f7f"),
    "yellow": get_color_from_hex("#ffc956"),
    "light_yellow": get_color_from_hex("#ffd67d"),
}
