from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label


class MainMenuButton(Button):
    def __init__(self, **kwargs):
        super(MainMenuButton, self).__init__(**kwargs)
        self.font_name = "Segoesc"
        self.bold = True
        self.font_size = 30


class MainMenuLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainMenuLayout, self).__init__(**kwargs)
        self.orientation = "vertical"

        # Add Image
        self.add_widget(Image(source="images/logo2.png"))

        # Add Label
        self.label = Label(text="BlackJack", color=(0, 0, 0, 1), font_size=40, bold=True, font_name="Segoesc")
        self.add_widget(self.label)

        # Add Buttons
        self.play_button = MainMenuButton(text="Play")
        self.add_widget(self.play_button)

        self.statistics_button = MainMenuButton(text="Player statistics")
        self.add_widget(self.statistics_button)

        self.exit_button = MainMenuButton(text="Exit")
        self.add_widget(self.exit_button)


class BlackJackGUI(App):

    def build(self):
        Window.clearcolor = (40/255, 40/255, 40/255, 40/255)
        return MainMenuLayout()


BlackJackGUI().run()
