from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from blackjack_game import BlackJackGame
from widgets import CustomLabel, CustomButton
from kivy.clock import Clock


class GameLayout(GridLayout):
    def __init__(self, screen_manager, **kwargs):
        self.game = BlackJackGame()
        self.screen_manager = screen_manager

        super(GameLayout, self).__init__(**kwargs)
        self.cols = 1
        self.navigation_layout = GridLayout()
        self.navigation_layout.cols = 6

        self.back_button = CustomButton(text="back")
        self.back_button.bind(on_press=self.back_to_menu)
        self.new_game_button = CustomButton(text="restart")
        self.new_game_button.bind(on_press=self.start_new_game)
        self.navigation_layout.add_widget(self.back_button)
        self.navigation_layout.add_widget(self.new_game_button)
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

        self.player_decision_layout = GridLayout(padding=20)
        self.player_decision_layout.cols = 7
        self.player_decision_layout.add_widget(Label())
        self.player_decision_layout.add_widget(Label())

        self.hit_button = CustomButton(text='hit')
        self.hit_button.bind(on_press=self.hit)
        self.double_button = CustomButton(text='double')
        self.stand_button = CustomButton(text='stand')
        self.stand_button.bind(on_press=self.stand)
        self.player_decision_layout.add_widget(self.hit_button)
        self.player_decision_layout.add_widget(self.double_button)
        self.player_decision_layout.add_widget(self.stand_button)
        self.player_decision_layout.add_widget(Label())
        self.player_decision_layout.add_widget(Label())
        self.add_widget(self.player_decision_layout)

    def back_to_menu(self, _):
        self.screen_manager.current = 'menu'

    def hit(self, _):
        self.game.player_hit()
        self.update_player_layout()
        self.update_player_score_layout()
        if self.game.player.has_blackjack() or self.game.player.is_lost():
            self.end_game()

    def stand(self, _):
        if self.game.dealer.has_blackjack():
            self.end_game()
        self.game.dealer_play()
        self.update_dealer_layout()
        self.update_dealer_score_layout()
        self.end_game()

    def update_dealer_layout(self):
        self.dealer_layout.clear_widgets()
        for card in self.game.dealer.hand:
            self.dealer_layout.add_widget(Image(source=card.get_image_path()))
        if self.dealer_layout not in self.children:
            self.add_widget(self.dealer_layout)

    def update_player_layout(self):
        self.player_layout.clear_widgets()
        for card in self.game.player.hand:
            self.player_layout.add_widget(Image(source=card.get_image_path()))
        if self.player_layout not in self.children:
            self.add_widget(self.player_layout)

    def update_player_score_layout(self):
        self.player_score_layout.clear_widgets()
        self.player_score_layout.add_widget(CustomLabel(text=self.game.player.__str__()))
        if self.player_score_layout not in self.children:
            self.add_widget(self.player_score_layout)

    def update_dealer_score_layout(self):
        self.dealer_score_layout.clear_widgets()
        self.dealer_score_layout.add_widget(CustomLabel(text=self.game.dealer.__str__()))
        if self.dealer_score_layout not in self.children:
            self.add_widget(self.dealer_score_layout)

    def end_game(self):
        winner = self.game.find_winner()
        self.show_popup(winner)

    @staticmethod
    def show_popup(message):
        def open_popup(_):
            popup = Popup(title='Game Over',
                          content=Label(text=message),
                          size_hint=(None, None), size=(400, 200))
            popup.open()

        # Schedule the popup to open after 3 seconds
        Clock.schedule_once(open_popup, 3)

    def start_new_game(self, _):
        self.game.start_game()


class MainMenuLayout(GridLayout):
    def __init__(self, screen_manager, **kwargs):
        self.screen_manager = screen_manager
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

        # Add "Play" button and bind to start_game
        self.play_button = CustomButton(text="Play")
        self.play_button.bind(on_press=self.start_game)
        self.add_widget(self.play_button)

        # Add "Practise" button and bind to ...
        self.practise_button = CustomButton(text="Practise basic strategy")
        self.add_widget(self.practise_button)

        # Add "Statistic" button and bind to ...
        self.statistics_button = CustomButton(text="Player statistics")
        self.add_widget(self.statistics_button)

        self.exit_button = CustomButton(text="Exit")
        self.add_widget(self.exit_button)

    def start_game(self, _):
        self.screen_manager.current = 'game'
