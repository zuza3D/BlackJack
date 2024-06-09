from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from blackjack_game import BlackJackGame
from widgets import CustomLabel, CustomButton, TitleLabel, CustomPopup, MenuButton, ScoreLabel, PopupLayout


class GameLayout(GridLayout):
    def __init__(self, screen_manager, **kwargs):
        self.game = BlackJackGame()
        self.screen_manager = screen_manager

        super(GameLayout, self).__init__(**kwargs)
        self.cols = 1
        self.navigation_layout = StackLayout(size_hint=(1, 0.4))

        self.popup = None

        self.back_button = CustomButton(text="menu".upper(), size_hint=(0.2, 1))
        self.back_button.bind(on_press=self.back_to_menu)
        self.new_game_button = CustomButton(text="new game".upper(), size_hint=(0.2, 1))
        self.new_game_button.bind(on_press=self.start_new_game)
        self.navigation_layout.add_widget(self.back_button)
        self.navigation_layout.add_widget(self.new_game_button)
        self.add_widget(self.navigation_layout)

        self.game.start_game()

        self.dealer_score_layout = GridLayout()
        self.dealer_score_layout.cols = 5
        self.update_dealer_score_layout()

        self.dealer_layout = StackLayout()
        self.update_dealer_layout()

        self.player_score_layout = GridLayout()
        self.player_score_layout.cols = 5
        self.update_player_score_layout()

        self.player_layout = StackLayout()
        self.update_player_layout()

        self.player_split_layout = StackLayout()
        self.update_player_layout()

        self.player_decision_layout = GridLayout(size_hint_y=0.4)
        self.player_decision_layout.cols = 7
        self.player_decision_layout.add_widget(Label())
        self.player_decision_layout.add_widget(Label())

        self.hit_button = CustomButton(text='hit'.upper())
        self.hit_button.bind(on_press=self.hit)
        self.double_button = CustomButton(text='double'.upper())
        self.stand_button = CustomButton(text='stand'.upper())
        self.stand_button.bind(on_press=self.stand)
        self.player_decision_layout.add_widget(self.hit_button)
        self.player_decision_layout.add_widget(self.double_button)
        self.player_decision_layout.add_widget(self.stand_button)
        self.player_decision_layout.add_widget(Label())
        self.player_decision_layout.add_widget(Label())
        self.add_widget(GridLayout(size_hint_y=0.2))
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

    def update_dealer_layout(self):
        self.dealer_layout.clear_widgets()
        dealer_cards = self.game.dealer.hand
        if self.game.dealer.hidden_card:
            self.dealer_layout.add_widget(Image(source=dealer_cards[0].get_image_path(), size_hint=(0.2, 1)))
            self.dealer_layout.add_widget(Image(source='images/cards/blank.png', size_hint=(0.2, 1)))
        else:
            for card in self.game.dealer.hand:
                self.dealer_layout.add_widget(Image(source=card.get_image_path(), size_hint=(0.2, 1)))
        if self.dealer_layout not in self.children:
            self.add_widget(self.dealer_layout)

    def update_player_layout(self):
        self.player_layout.clear_widgets()
        for card in self.game.player.hand:
            self.player_layout.add_widget(Image(source=card.get_image_path(), size_hint=(0.2, 1)))
        if self.player_layout not in self.children:
            self.add_widget(self.player_layout)

    def update_player_score_layout(self):
        self.player_score_layout.clear_widgets()
        self.player_score_layout.add_widget(ScoreLabel(text=self.game.player.__str__().upper()))
        if self.player_score_layout not in self.children:
            self.add_widget(self.player_score_layout)

    def update_dealer_score_layout(self):
        self.dealer_score_layout.clear_widgets()
        self.dealer_score_layout.add_widget(ScoreLabel(text=self.game.dealer.__str__().upper()))
        if self.dealer_score_layout not in self.children:
            self.add_widget(self.dealer_score_layout)

    def end_game(self):
        winner = self.game.find_winner()
        result = self.game.show_result()
        self.show_popup(winner, result)

    def show_popup(self, title, content):
        self.popup = CustomPopup(title=title)
        self.popup.content = content=PopupLayout(details=content, game_layout=self, popup=self.popup)
        self.popup.open()

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


class MainMenuLayout(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        self.screen_manager = screen_manager
        super(MainMenuLayout, self).__init__(**kwargs)
        self.padding = 20
        self.spacing = 20

        self.orientation = 'vertical'

        self.add_widget(TitleLabel())

        # Add "Play" button and bind to start_game
        self.play_button = MenuButton(text="Play".upper())
        self.play_button.bind(on_press=self.start_game)
        self.add_widget(self.play_button)

        # Add "Practise" button
        self.practise_button = MenuButton(text="Practise basic strategy".upper())
        self.add_widget(self.practise_button)

        # Add "Statistic" button
        self.statistics_button = MenuButton(text="Player statistics".upper())
        self.add_widget(self.statistics_button)

        # Add "Exit" button
        self.exit_button = MenuButton(text="Exit".upper())
        self.add_widget(self.exit_button)

    def start_game(self, _):
        self.screen_manager.current = 'game'
