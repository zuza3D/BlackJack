from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from blackjack_game import BlackJackGame


class CustomButton(Button):
    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.font_name = "Comic"
        self.bold = True
        self.font_size = 30


class GameLayout(GridLayout):
    def __init__(self, **kwargs):
        self.game = BlackJackGame()

        super(GameLayout, self).__init__(**kwargs)
        self.cols = 1
        self.navigation_layout = GridLayout()
        self.navigation_layout.cols = 6

        self.back_button = CustomButton(text="<-")
        self.back_button.bind(on_press=self.back_to_menu)
        self.navigation_layout.add_widget(self.back_button)
        self.navigation_layout.add_widget(Label())
        self.navigation_layout.add_widget(Label())
        self.navigation_layout.add_widget(Label())
        self.add_widget(self.navigation_layout)

        self.game.start_game()

        self.dealer_score_layout = GridLayout()
        self.dealer_score_layout.cols = 5
        self.update_dealer_score_layout()

        self.dealer_layout = GridLayout()
        self.dealer_layout.cols = 5
        for card in self.game.dealer.hand:
            self.dealer_layout.add_widget(Image(source=card.get_image_path()))
        self.add_widget(self.dealer_layout)

        self.player_score_layout = GridLayout()
        self.player_score_layout.cols = 5
        self.update_player_score_layout()

        self.player_layout = GridLayout()
        self.player_layout.cols = 5
        self.update_player_layout()

        self.player_decision_layout = GridLayout()
        self.player_decision_layout.cols = 7
        self.player_decision_layout.add_widget(Label())
        self.player_decision_layout.add_widget(Label())

        self.hit_button = CustomButton(text='hit')
        self.hit_button.bind(on_press=self.hit)
        self.double_button = CustomButton(text='double')
        self.stand_button = CustomButton(text='stand')
        self.player_decision_layout.add_widget(self.hit_button)
        self.player_decision_layout.add_widget(self.double_button)
        self.player_decision_layout.add_widget(self.stand_button)
        self.player_decision_layout.add_widget(Label())
        self.player_decision_layout.add_widget(Label())
        self.add_widget(self.player_decision_layout)

    def back_to_menu(self, item):
        black_jack_gui.screen_manager.current = 'menu'

    def hit(self, item):
        self.game.player_hit()
        self.update_player_layout()
        self.update_player_score_layout()

    def update_player_layout(self):
        self.player_layout.clear_widgets()
        for card in self.game.player.hand:
            self.player_layout.add_widget(Image(source=card.get_image_path()))
        if self.player_layout not in self.children:
            self.add_widget(self.player_layout)

    def update_player_score_layout(self):
        self.player_score_layout.clear_widgets()
        self.player_score_layout.add_widget(Label(text=self.game.player.__str__()))
        if self.player_score_layout not in self.children:
            self.add_widget(self.player_score_layout)

    def update_dealer_score_layout(self):
        self.dealer_score_layout.clear_widgets()
        self.dealer_score_layout.add_widget(Label(text=self.game.dealer.__str__()))
        if self.dealer_score_layout not in self.children:
            self.add_widget(self.dealer_score_layout)

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
        self.play_button = CustomButton(text="Play")
        self.play_button.bind(on_press=self.start_game)
        self.add_widget(self.play_button)

        self.train_button = CustomButton(text="Practise basic strategy")
        self.add_widget(self.train_button)

        self.statistics_button = CustomButton(text="Player statistics")
        self.add_widget(self.statistics_button)

        self.exit_button = CustomButton(text="Exit")
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
        Window.clearcolor = (40 / 255, 40 / 255, 40 / 255, 40 / 255)

        screen = Screen(name="menu")
        screen.add_widget(self.menu_page)
        self.screen_manager.add_widget(screen)

        screen = Screen(name="game")
        screen.add_widget(self.game_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


black_jack_gui = BlackJackGUI()
black_jack_gui.run()
