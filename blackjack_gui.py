from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from blackjack_game import BlackJackGame
from widgets import CustomLabel, CustomButton, MenuLabel, CustomPopup
from kivy.clock import Clock


class GameLayout(GridLayout):
    def __init__(self, screen_manager, **kwargs):
        self.game = BlackJackGame()
        self.screen_manager = screen_manager

        super(GameLayout, self).__init__(**kwargs)
        self.cols = 1
        self.navigation_layout = GridLayout(size_hint_y=0.4)
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
        self.update_dealer_layout()

        self.player_score_layout = GridLayout()
        self.player_score_layout.cols = 5
        self.update_player_score_layout()

        self.player_layout = GridLayout()
        self.player_layout.cols = 5
        self.update_player_layout()

        self.player_decision_layout = GridLayout(size_hint_y=0.4)
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
        self.load_new_game()
        self.screen_manager.current = 'menu'

    def hit(self, _):
        self.game.player_hit()
        self.update_player_layout()
        self.update_player_score_layout()
        if self.game.is_game_over():
            self.end_game()

    def stand(self, _):
        if self.game.dealer.has_blackjack():
            self.end_game()
        self.game.dealer_play()
        self.update_dealer_layout()
        self.update_dealer_score_layout()
        self.end_game()

    def update_dealer_layout(self, hide_cards=True):
        self.dealer_layout.clear_widgets()
        dealer_cards = self.game.dealer.hand
        if self.game.dealer.hidden_card:
            self.dealer_layout.add_widget(Image(source=dealer_cards[0].get_image_path()))
            self.dealer_layout.add_widget(Image(source='images/cards/blank.png'))
        else:
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
            popup = CustomPopup(content=CustomLabel(text=message))
            popup.open()

        # Schedule the popup to open after 2 seconds
        Clock.schedule_once(open_popup, 2)

    def load_new_game(self):
        self.game.start_game()
        self.update_player_layout()
        self.update_dealer_layout()
        self.update_player_score_layout()
        self.update_dealer_score_layout()
        if self.game.is_game_over():
            self.end_game()

    def start_new_game(self, _):
        self.game.start_game()
        self.update_player_layout()
        self.update_dealer_layout()
        self.update_player_score_layout()
        self.update_dealer_score_layout()
        if self.game.is_game_over():
            self.end_game()


class MainMenuLayout(GridLayout):
    def __init__(self, screen_manager, **kwargs):
        self.screen_manager = screen_manager
        super(MainMenuLayout, self).__init__(**kwargs)
        self.cols = 1
        self.padding = 20
        self.spacing = 20

        self.top_grid = GridLayout(size_hint_y=0.4)
        self.top_grid.cols = 1

        # Add Image
        self.top_grid.add_widget(Image(source="images/logoo.png"))

        # Add Label
        # self.label = MenuLabel()
        # self.top_grid.add_widget(self.label)

        # Add Image
        # self.top_grid.add_widget(Image(source="images/logo_r.png"))

        self.add_widget(self.top_grid)

        self.buttons_layout = GridLayout()
        self.buttons_layout.cols = 1
        # Add "Play" button and bind to start_game
        self.play_button = CustomButton(text="Play")
        self.play_button.bind(on_press=self.start_game)
        self.buttons_layout.add_widget(self.play_button)

        # Add "Practise" button and bind to ...
        self.practise_button = CustomButton(text="Practise basic strategy")
        self.buttons_layout.add_widget(self.practise_button)

        # Add "Statistic" button and bind to ...
        self.statistics_button = CustomButton(text="Player statistics")
        self.buttons_layout.add_widget(self.statistics_button)

        self.exit_button = CustomButton(text="Exit")
        self.buttons_layout.add_widget(self.exit_button)

        self.add_widget(self.buttons_layout)

    def start_game(self, _):
        self.screen_manager.current = 'game'
