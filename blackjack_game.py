from deck_of_card import DeckOfCard
from card import Card, CardRank


class Player:
    hand: list[Card]
    extra_point_ace: bool
    higher_score: int
    lower_score: int

    def __init__(self):
        self.hand = list()
        self.extra_point_ace = False
        self.higher_score = 0
        self.lower_score = 0

    def take_card(self, card):
        self.hand.append(card)

        card_value = card.get_value()
        card_rank = card.get_rank()

        self.lower_score += card_value
        self.higher_score += card_value
        self.higher_score += (10 if card_rank == CardRank.Ace and
                                    not self.extra_point_ace else 0)
        if card_rank == CardRank.Ace and not self.extra_point_ace:
            self.extra_point_ace = True

    def reset(self):
        self.hand.clear()
        self.extra_point_ace = False
        self.higher_score = 0
        self.lower_score = 0

    def __str__(self):
        return f'Player: {self.higher_score} | {self.lower_score}'


class Dealer(Player):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'Dealer: {self.higher_score} | {self.lower_score}'


class BlackJackGame:
    deck_of_card: DeckOfCard
    dealer: Dealer
    player: Player
    player_hand: list[Card]

    def __init__(self):
        self.deck_of_card = DeckOfCard()
        self.dealer = Dealer()
        self.player = Player()

    def start_game(self):
        self.dealer.reset()
        self.player.reset()
        self.deck_of_card.shuffle()
        self.deal_initial_cards()

    def deal_initial_cards(self):
        for i in range(2):
            self.dealer.take_card(self.deck_of_card.deal_card())
            self.player.take_card(self.deck_of_card.deal_card())

    def player_hit(self):
        self.player.take_card(self.deck_of_card.deal_card())

    def dealer_play(self):
        while self.dealer.higher_score < 17 and self.dealer.lower_score < 17:
            self.dealer.take_card(self.deck_of_card.deal_card())
        while self.dealer.lower_score < 17:
            self.dealer.take_card(self.deck_of_card.deal_card())

    def find_winner(self):
        player_best_result = (self.player.lower_score if self.player.higher_score > 21
                              else self.player.higher_score)
        dealer_best_result = (self.dealer.lower_score if self.dealer.higher_score > 21
                              else self.dealer.higher_score)

        if player_best_result > 21:
            return f'Dealer wins'
        if dealer_best_result > 21:
            return f'Player wins'
        if player_best_result > dealer_best_result:
            return f'Player wins'
        if dealer_best_result > player_best_result:
            return f'Dealer wins'
        return "It's a tie!"
