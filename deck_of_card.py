import random

from card import CardRank, CardSuit, Card


class DeckOfCard:
    _deck: list[Card]

    def __init__(self):
        self._deck = [Card(value, suit) for value in CardRank for suit in CardSuit]

    def __repr__(self):
        return ', '.join([card.__repr__() for card in self._deck])

    def get_deck(self):
        return self._deck

    def shuffle(self):
        random.shuffle(self._deck)

    def deal_card(self):
        self._deck.pop()

