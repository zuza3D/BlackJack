from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class CustomButton(Button):
    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.font_name = "Comic"
        self.bold = True
        self.font_size = 25
        self.color = (240 / 255, 215 / 255, 135 / 255, 1)
        self.background_color = (110 / 255, 10 / 255, 60 / 255, 1)


class CustomLabel(Label):
    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
        self.font_name = "Comic"
        self.font_size = 25
        self.color = (110 / 255, 10 / 255, 60 / 255, 1)


class MenuLabel(Label):
    def __init__(self, **kwargs):
        super(MenuLabel, self).__init__(**kwargs)
        self.font_name = "Comic"
        self.text = "BlackJack"
        self.font_size = 50
        self.bold = True
        self.color = (110 / 255, 10 / 255, 60 / 255, 1)


class CustomPopup(Popup):
    def __init__(self, **kwargs):
        super(CustomPopup, self).__init__(**kwargs)
        self.title = 'Game Over'
        self.size_hint = (None, None)
        self.size = (400, 200)
        self.background_color = (240 / 255, 215 / 255, 135 / 255, 1)
        self.title_color = (110 / 255, 10 / 255, 60 / 255, 1)
        self.title_font = "Comic"
        self.title_align = "center"
        self.title_size = 50
