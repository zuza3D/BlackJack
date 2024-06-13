import random

from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget

from game.basic_strategy import BasicStrategy
from game.card import Card, CardSuit, CardRank
from gui.widgets import CustomButton, CustomLabel, CustomPopup, QuizPopup


class QuizLayout(GridLayout):
    def __init__(self, screen_manager, **kwargs):
        super(QuizLayout, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.basic_strategy = BasicStrategy()
        self.cols = 1
        self.popup = None

        self.suits = list(CardSuit)
        self.ranks = list(CardRank)
        self.dealer_card = None
        self.player_hand = []

        self.navigation_bar = StackLayout(size_hint=(1, 0.2))

        self.back_button = CustomButton(text="menu".upper(), size_hint=(0.2, 1))
        self.back_button.bind(on_press=self.back_to_menu)
        self.navigation_bar.add_widget(self.back_button)

        self.random_button = CustomButton(text="random question".upper(), size_hint=(0.5, 1))
        self.random_button.bind(on_press=self.random_question)
        self.navigation_bar.add_widget(self.random_button)
        self.navigation_bar.add_widget(CustomLabel(text="Basic strategy".upper(), size_hint=(0.3, 1)))
        self.add_widget(self.navigation_bar)
        self.dealer_layout = StackLayout(padding=20, spacing=20)
        self.player_layout = StackLayout(padding=20, spacing=20)
        self.update_cards_layout()

        self.decision_layout = self.create_decision_layout()
        self.add_widget(self.decision_layout)

    def create_decision_layout(self):
        decision_layout = StackLayout(size_hint=(1, 0.3))
        stand_button = CustomButton(text="stand".upper(), size_hint=(0.25, 1))
        stand_button.bind(on_press=self.check_answer)
        hit_button = CustomButton(text="hit".upper(), size_hint=(0.25, 1))
        hit_button.bind(on_press=self.check_answer)
        double_button = CustomButton(text="double".upper(), size_hint=(0.25, 1))
        double_button.bind(on_press=self.check_answer)
        split_button = CustomButton(text="split".upper(), size_hint=(0.25, 1))
        split_button.bind(on_press=self.check_answer)

        decision_layout.add_widget(stand_button)
        decision_layout.add_widget(hit_button)
        decision_layout.add_widget(double_button)
        decision_layout.add_widget(split_button)

        return decision_layout

    def back_to_menu(self, _):
        self.screen_manager.current = 'menu'

    def random_question(self, _):
        self.update_cards_layout()

    def update_cards_layout(self):
        self.player_hand.clear()
        self.player_layout.clear_widgets()
        self.dealer_layout.clear_widgets()
        self.dealer_layout.add_widget(CustomLabel(text='dealer'.upper(), size_hint=(0.14, 0.8)))
        self.player_layout.add_widget(CustomLabel(text='player'.upper(), size_hint=(0.14, 0.8)))
        self.dealer_layout.add_widget(Widget(size_hint=(0.14, 0.8)))
        self.player_layout.add_widget(Widget(size_hint=(0.14, 0.8)))
        card = Card(rank=random.choice(self.ranks), suit=random.choice(self.suits))
        self.dealer_card = card
        self.dealer_layout.add_widget(Image(source=card.get_image_path(), size_hint=(0.2, 0.8)))
        self.dealer_layout.add_widget(Image(source='images/cards/blank.png', size_hint=(0.2, 0.8)))

        for i in range(2):
            card = Card(rank=random.choice(self.ranks), suit=random.choice(self.suits))
            self.player_hand.append(card)
            self.player_layout.add_widget(Image(source=card.get_image_path(), size_hint=(0.2, 0.8)))

        if self.dealer_layout not in self.children:
            self.add_widget(self.dealer_layout)
        if self.player_layout not in self.children:
            self.add_widget(self.player_layout)

    def check_answer(self, instance):
        selected_option = instance.text.lower()
        good_answer = self.basic_strategy.get_action(self.player_hand, self.dealer_card)
        result = selected_option == good_answer
        if result:
            self.show_popup("Correct!", f'{selected_option.upper()} is a good answer')
        else:
            self.show_popup("Try again!", f'{good_answer.upper()} is a good answer')

    def show_popup(self, title, content):
        self.popup = CustomPopup(title=title)
        self.popup.content = QuizPopup(details=content, popup=self.popup, quiz_layout=self)
        self.popup.open()
