from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout

from game.blackjack_game import BlackJackGame
from gui.widgets import CustomButton, TitleLabel, CustomPopup, CenteredButton, PopupLayout, CustomLabel, CustomIntSlider, \
    CreditsLabel


class GameLayout(GridLayout):
    def __init__(self, screen_manager, player_stats, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        self.bet_label = None
        self.bet_button = None
        self.slider = None
        self.cols = 1

        self.screen_manager = screen_manager
        self.game = BlackJackGame()
        self.player_stats = player_stats

        self.popup = None

        self.navigation_bar = StackLayout(size_hint=(1, 0.4))

        self.back_button = CustomButton(text="menu".upper(), size_hint=(0.2, 1))
        self.back_button.bind(on_press=self.back_to_menu)
        self.new_game_button = CustomButton(text="new game".upper(), size_hint=(0.2, 1))
        self.new_game_button.bind(on_press=self.start_new_game)
        self.credits_label = CreditsLabel(self.player_stats.balance)
        self.navigation_bar.add_widget(self.back_button)
        self.navigation_bar.add_widget(self.new_game_button)
        self.navigation_bar.add_widget(self.credits_label)
        self.add_widget(self.navigation_bar)

        self.game.start_game()

        self.dealer_score_layout = GridLayout()
        self.dealer_score_layout.cols = 5
        # self.update_dealer_score_layout()

        self.dealer_layout = StackLayout()
        # self.update_dealer_layout()

        self.player_score_layout = GridLayout()
        self.player_score_layout.cols = 5
        # self.update_player_score_layout()

        self.player_layout = StackLayout()
        # self.update_player_layout()
        self.create_empty_table()

        self.player_decision_bar = GridLayout(size_hint_y=0.4)
        self.player_decision_bar.cols = 7
        self.player_decision_bar.add_widget(Label())
        self.player_decision_bar.add_widget(Label())

        self.hit_button = CustomButton(text='hit'.upper())
        self.hit_button.bind(on_press=self.hit)
        self.double_button = CustomButton(text='double'.upper())
        self.stand_button = CustomButton(text='stand'.upper())
        self.stand_button.bind(on_press=self.stand)
        self.player_decision_bar.add_widget(self.hit_button)
        self.player_decision_bar.add_widget(self.double_button)
        self.player_decision_bar.add_widget(self.stand_button)
        self.player_decision_bar.add_widget(Label())
        self.player_decision_bar.add_widget(Label())
        self.add_widget(GridLayout(size_hint_y=0.2))
        self.add_widget(self.player_decision_bar)

        self.bet_bar = BoxLayout()
        self.bet_bar.orientation = 'vertical'
        self.create_bet_bar()
        self.add_widget(self.bet_bar)

        # self.xd = StackLayout()
        # self.xd.add_widget(CustomButton(background_color=(1,0,0,1), size_hint=(0.2, 1)))
        # self.xd.add_widget(CustomButton(background_color=(0, 1, 0, 1), size_hint=(0.8, 1)))
        # self.add_widget(self.xd)

    def create_empty_table(self):
        self.update_dealer_score_layout(before_bet=True)
        self.update_dealer_layout(before_bet=True)
        self.update_player_score_layout(before_bet=True)
        self.update_player_layout(before_bet=True)

    def create_bet_bar(self):
        self.bet_bar.clear_widgets()
        self.disable_player_decision_buttons()
        self.slider = CustomIntSlider(max=self.player_stats.balance)
        self.slider.bind(value=self.on_slider_value_change)

        self.bet_button = CenteredButton(text='Bet'.upper())
        self.bet_button.bind(on_press=lambda instance: self.on_button_press(self.slider.value))

        self.bet_label = CustomLabel()

        self.bet_bar.add_widget(self.slider)
        self.bet_bar.add_widget(self.bet_label)
        self.on_slider_value_change(self.slider, self.slider.value)
        self.bet_bar.add_widget(self.bet_button)

    def on_slider_value_change(self, instance, value):
        self.bet_label.text = str(self.slider.value) + "$"

    def update_credits_label(self):
        self.credits_label.text = "credits: ".upper() + str(self.player_stats.balance) + "$"

    def on_button_press(self, value):
        self.update_dealer_score_layout()
        self.update_dealer_layout()
        self.update_player_score_layout()
        self.update_player_layout()
        self.player_stats.balance -= value
        self.game.player.bet = value
        self.update_credits_label()
        self.bet_bar.clear_widgets()
        self.enable_player_decision_buttons()
        if self.game.is_game_over():
            self.end_game()

    def disable_player_decision_buttons(self):
        for child in self.player_decision_bar.children:
            if isinstance(child, CustomButton):
                child.disabled = True

    def enable_player_decision_buttons(self):
        for child in self.player_decision_bar.children:
            if isinstance(child, CustomButton):
                child.disabled = False

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
            return
        self.game.dealer_play()
        self.update_dealer_layout()
        self.update_dealer_score_layout()
        self.end_game()

    def update_dealer_layout(self, before_bet=False):
        self.dealer_layout.clear_widgets()
        dealer_cards = self.game.dealer.hand
        if before_bet:
            for card in self.game.dealer.hand:
                self.dealer_layout.add_widget(Image(source='images/cards/blank.png', size_hint=(0.2, 1)))
        else:
            if self.game.dealer.hidden_card:
                self.dealer_layout.add_widget(Image(source=dealer_cards[0].get_image_path(), size_hint=(0.2, 1)))
                self.dealer_layout.add_widget(Image(source='images/cards/blank.png', size_hint=(0.2, 1)))
            else:
                for card in self.game.dealer.hand:
                    self.dealer_layout.add_widget(Image(source=card.get_image_path(), size_hint=(0.2, 1)))
        if self.dealer_layout not in self.children:
            self.add_widget(self.dealer_layout)

    def update_player_layout(self, before_bet=False):
        self.player_layout.clear_widgets()
        for card in self.game.player.hand:
            if before_bet:
                self.player_layout.add_widget(Image(source='images/cards/blank.png', size_hint=(0.2, 1)))
            else:
                self.player_layout.add_widget(Image(source=card.get_image_path(), size_hint=(0.2, 1)))
        if self.player_layout not in self.children:
            self.add_widget(self.player_layout)

    def update_player_score_layout(self, before_bet=False):
        self.player_score_layout.clear_widgets()
        if before_bet:
            self.player_score_layout.add_widget(CustomLabel(text="Player: ".upper()))
        else:
            self.player_score_layout.add_widget(CustomLabel(text=self.game.player.__str__().upper()))
        if self.player_score_layout not in self.children:
            self.add_widget(self.player_score_layout)

    def update_dealer_score_layout(self, before_bet=False):
        self.dealer_score_layout.clear_widgets()
        if before_bet:
            self.dealer_score_layout.add_widget(CustomLabel(text="Dealer: ".upper()))
        else:
            self.dealer_score_layout.add_widget(CustomLabel(text=self.game.dealer.__str__().upper()))
        if self.dealer_score_layout not in self.children:
            self.add_widget(self.dealer_score_layout)

    def end_game(self):
        self.update_dealer_layout()
        self.update_dealer_score_layout()
        self.game.update_result()
        winner = self.game.find_winner()
        result = self.game.show_result()
        self.player_stats.update_stats(self.game.result, self.game.player.bet, blackjack=False)
        if self.player_stats.balance == 0:
            self.show_popup("game over".upper(), self.player_stats.show_statistics())
            self.player_stats.reset_statistics()
        else:
            self.show_popup(winner, result)

    def show_popup(self, title, content):
        self.popup = CustomPopup(title=title)
        self.popup.content = PopupLayout(details=content, game_layout=self, popup=self.popup)
        self.popup.open()

    def _initialize_game(self):
        self.game.start_game()
        self.update_credits_label()
        self.create_empty_table()
        self.create_bet_bar()
        # if self.game.is_game_over():
        #     self.end_game()

    def load_new_game(self):
        self._initialize_game()

    def start_new_game(self, _):
        self._initialize_game()


class MainMenuLayout(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        self.screen_manager = screen_manager
        super(MainMenuLayout, self).__init__(**kwargs)
        self.padding = 20
        self.spacing = 20

        self.orientation = 'vertical'

        self.add_widget(TitleLabel())

        # Add "Play" button and bind to start_game
        self.play_button = CenteredButton(text="Play".upper())
        self.play_button.bind(on_press=self.start_game)
        self.add_widget(self.play_button)

        # Add "Practise" button
        self.practise_button = CenteredButton(text="Practise basic strategy".upper())
        self.add_widget(self.practise_button)

        # Add "Statistic" button
        self.statistics_button = CenteredButton(text="Player statistics".upper())
        self.add_widget(self.statistics_button)

        # Add "Exit" button
        self.exit_button = CenteredButton(text="Exit".upper())
        self.add_widget(self.exit_button)

    def start_game(self, _):
        self.screen_manager.current = 'game'
