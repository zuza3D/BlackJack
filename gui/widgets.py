from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider


class CustomButton(Button):
    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.font_name = "Comic"
        self.bold = True
        self.font_size = 25
        self.color = (240 / 255, 215 / 255, 135 / 255, 1)
        self.background_color = (110 / 255, 10 / 255, 60 / 255, 1)
        self.disabled_color = (240 / 255, 215 / 255, 135 / 255, 1)


class CenteredButton(CustomButton):
    def __init__(self, **kwargs):
        super(CenteredButton, self).__init__(**kwargs)
        self.size_hint_x = 0.5
        self.pos_hint = {'center_x': 0.5}


class CustomLabel(Label):
    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
        self.font_name = "Comic"
        self.font_size = 25
        self.color = (240 / 255, 215 / 255, 135 / 255, 1)


class TitleLabel(Label):
    def __init__(self, **kwargs):
        super(TitleLabel, self).__init__(**kwargs)
        self.font_name = "Comic"
        self.text = "BlackJack"
        self.font_size = 50
        self.bold = True
        self.color = (240 / 255, 215 / 255, 135 / 255, 1)


class CustomPopup(Popup):
    def __init__(self, **kwargs):
        super(CustomPopup, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (400, 230)
        self.background_color = (114 / 255, 13 / 255, 80 / 255, 1)
        self.title_color = (240 / 255, 215 / 255, 135 / 255, 1)
        self.title_font = "Comic"
        self.title_align = "center"
        self.title_size = 40
        self.separator_color = (240 / 255, 215 / 255, 135 / 255, 1)


class PopupLayout(BoxLayout):
    def __init__(self, details, game_layout, popup, **kwargs):
        super(PopupLayout, self).__init__(**kwargs)
        self.game_layout = game_layout
        self.popup = popup
        self.orientation = "vertical"
        self.add_widget(CustomLabel(text=details))
        self.button = PopupButton(text="play again", size_hint_y=0.5)
        self.button.bind(on_press=self.close_popup)
        self.button.bind(on_press=self.game_layout.start_new_game)
        self.add_widget(self.button)
        self.game_layout.disable_player_decision_buttons()

    def close_popup(self, _):
        self.popup.dismiss()


class PopupButton(CenteredButton):
    def __init__(self, **kwargs):
        super(PopupButton, self).__init__(**kwargs)
        self.background_color = (240 / 255, 215 / 255, 135 / 255, 1)
        self.color = (38 / 255, 3 / 255, 21 / 255, 1)


class CustomSlider(Slider):
    def __init__(self, **kwargs):
        super(CustomSlider, self).__init__(**kwargs)
        self.min = 1
        self.value = int(self.max / 2) if self.max > 1 else 1
        self.step = 1
        self.value = int(self.value)
        self.value_track = True
        self.value_track_color = (110 / 255, 10 / 255, 60 / 255, 1)
        self.handle_color = (110 / 255, 10 / 255, 60 / 255, 1)
        self.cursor_image = "images/slider_image.png"


class CreditsLabel(CustomLabel):
    def __init__(self, balance, **kwargs):
        super(CreditsLabel, self).__init__(**kwargs)
        self.text = "credits: ".upper() + str(balance) + "$"
        self.size_hint = (0.4, 1)
