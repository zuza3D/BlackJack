from kivy.uix.button import Button
from kivy.uix.label import Label


class CustomButton(Button):
    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.font_name = "Comic"
        self.bold = True
        self.font_size = 25


class CustomLabel(Label):
    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
        self.font_name = "Comic"
        self.font_size = 25
