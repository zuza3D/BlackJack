from typing import Dict

from deck_of_card import DeckOfCard
from card import Card, CardRank


class Player:
    _hand: list[Card]
    _extra_point_ace: bool
    _score: int
    _bet: int

    def __init__(self):
        self._hand = list()
        self._extra_point_ace = False
        self._score = 0
        self._bet = 0

    @property
    def bet(self):
        return self._bet

    @bet.setter
    def bet(self, value):
        self._bet = value
    @property
    def hand(self):
        return self._hand

    @property
    def score(self):
        return self._score

    @property
    def extra_point_ace(self):
        return self._extra_point_ace

    def reset_bet(self):
        self._bet = 0

    def take_card(self, card):
        self._hand.append(card)

        card_value = card.get_value()
        card_rank = card.get_rank()

        self._score += card_value
        if card_rank == CardRank.Ace and not self._extra_point_ace:
            self._extra_point_ace = True

    def reset(self):
        self._hand.clear()
        self._extra_point_ace = False
        self._score = 0

    def __str__(self):
        return (f'Player: {self._score} | {self._score + 10}' if self._extra_point_ace
                else f'Player: {self._score}')

    def is_lost(self):
        return True if self._score > 21 else False

    def has_blackjack(self):
        return True if self._score == 21 or self._score + self._extra_point_ace * 10 == 21 else False


class Dealer(Player):
    _hidden_card: bool

    def __init__(self):
        super().__init__()
        self._hidden_card = True

    def __str__(self):
        if self._hidden_card:
            return f'Dealer: {self.get_visible_score()} '
        return (f'Dealer: {self._score} | {self._score + 10}' if self._extra_point_ace
                else f'Dealer: {self._score}')

    def reveal_card(self):
        self._hidden_card = False

    def get_visible_score(self):
        if self._hidden_card:
            return self._hand[0].get_value() if self._hand[0].get_rank() != CardRank.Ace \
                else self._hand[0].get_value() + 10
        return self._score

    def hide_card(self):
        self._hidden_card = True

    @property
    def hidden_card(self):
        return self._hidden_card


class BlackJackGame:
    _deck_of_card: DeckOfCard
    _dealer: Dealer
    _player: Player
    _result: Dict

    def __init__(self):
        self._deck_of_card = DeckOfCard()
        self._dealer = Dealer()
        self._player = Player()
        self._result = {'player': 0, 'dealer': 0, 'tie': 0}

    @property
    def deck_of_card(self):
        return self._deck_of_card

    @property
    def dealer(self):
        return self._dealer

    @property
    def player(self):
        return self._player

    @property
    def result(self):
        return self._result

    def start_game(self):
        self._result = {'player': 0, 'dealer': 0, 'tie': 0}
        self._player.reset_bet()
        self._dealer.reset()
        self._dealer.hide_card()
        self._player.reset()
        self._deck_of_card = DeckOfCard()
        self._deck_of_card.shuffle()
        self.deal_initial_cards()

    def deal_initial_cards(self):
        for i in range(2):
            self._dealer.take_card(self._deck_of_card.deal_card())
            self._player.take_card(self._deck_of_card.deal_card())

    def player_hit(self):
        self._player.take_card(self._deck_of_card.deal_card())

    def dealer_play(self):
        self._dealer.reveal_card()
        while self._dealer.score + self._dealer.extra_point_ace * 10 < 17 and self._dealer.score < 17:
            self._dealer.take_card(self._deck_of_card.deal_card())
        while self._dealer.score + self._dealer.extra_point_ace * 10 > 21 and self._dealer.score < 17:
            self._dealer.take_card(self._deck_of_card.deal_card())

    def get_players_score(self):
        player_ace = self._player.extra_point_ace
        dealer_ace = self._dealer.extra_point_ace
        player_score = self._player.score + player_ace * 10
        dealer_score = self._dealer.score + dealer_ace * 10

        player_score = player_score if player_score <= 21 else player_score - player_ace * 10
        dealer_score = dealer_score if dealer_score <= 21 else dealer_score - dealer_ace * 10
        return player_score, dealer_score

    def find_winner(self):
        player_score, dealer_score = self.get_players_score()

        if player_score > 21:
            return f'Dealer wins'
        if dealer_score > 21:
            return f'Player wins'
        if player_score > dealer_score:
            return f'Player wins'
        if dealer_score > player_score:
            return f'Dealer wins'
        return "It's a tie!"

    # def find_winner(self):
    #     if self._result['player']:
    #         return f'Player wins'
    #     if self._result['dealer']:
    #         return f'Dealer wins'
    #     if self._result['tie']:
    #         return "It's a tie!"
    #     return "xd"

    def update_result(self):
        player_score, dealer_score = self.get_players_score()
        print(f'player{player_score}, dealer{dealer_score}')
        if player_score > 21:
            self._result['dealer'] = 1
        elif dealer_score > 21:
            self._result['player'] = 1
        elif player_score > dealer_score:
            self._result['player'] = 1
        elif dealer_score > player_score:
            self._result['dealer'] = 1
        else:
            self._result['tie'] = 1

    def is_game_over(self):
        if self._player.is_lost() or self._player.has_blackjack():
            return True
        return False

    def show_result(self):
        player_score, dealer_score = self.get_players_score()
        return f"Your hand: {player_score} \nDealer's hand: {dealer_score}"