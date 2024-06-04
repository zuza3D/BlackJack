from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition


class MainMenuButton(Button):
    def __init__(self, **kwargs):
        super(MainMenuButton, self).__init__(**kwargs)
        self.font_name = "Comic"
        self.bold = True
        self.font_size = 30


class GameLayout(GridLayout):
    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        self.cols = 1
        self.label = Label(text="hello")
        self.add_widget(self.label)


class MainMenuLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MainMenuLayout, self).__init__(**kwargs)
        self.cols = 1
        self.padding = 50
        self.spacing = 10

        self.top_grid = GridLayout()
        self.top_grid.cols = 3

        # Add Image
        self.top_grid.add_widget(Image(source="images/logo_l.png"))

        # Add Label
        self.label = Label(text="BlackJack", color=(0, 0, 0, 1), font_size=50, bold=True, font_name="Comic")
        self.top_grid.add_widget(self.label)

        # Add Image
        self.top_grid.add_widget(Image(source="images/logo_r.png"))

        self.add_widget(self.top_grid)

        # Add Buttons
        self.play_button = MainMenuButton(text="Play")
        self.play_button.bind(on_press=self.start_game)
        self.add_widget(self.play_button)

        self.train_button = MainMenuButton(text="Practise basic strategy")
        self.add_widget(self.train_button)

        self.statistics_button = MainMenuButton(text="Player statistics")
        self.add_widget(self.statistics_button)

        self.exit_button = MainMenuButton(text="Exit")
        self.add_widget(self.exit_button)

    def start_game(self, item):
        black_jack_gui.screen_manager.current = 'game'


class BlackJackGUI(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()
        self.menu_page = MainMenuLayout()
        self.game_page = GameLayout()

    def build(self):
        Window.clearcolor = (40/255, 40/255, 40/255, 40/255)

        screen = Screen(name="menu")
        screen.add_widget(self.menu_page)
        self.screen_manager.add_widget(screen)

        screen = Screen(name="game")
        screen.add_widget(self.game_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


black_jack_gui = BlackJackGUI()
black_jack_gui.run()
