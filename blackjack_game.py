from deck_of_card import DeckOfCard
from card import Card, CardRank


class Player:
    hand: list[Card]
    aces: int
    higher_score: int
    lower_score: int

    def __init__(self):
        self.hand = list()
        self.aces = 0
        self.higher_score = 0
        self.lower_score = 0

    def take_card(self, card):
        self.hand.append(card)
        if card == CardRank.Ace:
            self.aces += 1

        self.higher_score += (card.get_value() + 10 if card == CardRank.Ace and self.aces == 1
                              else card.get_value())

        self.lower_score += 1 if card == CardRank.Ace else card.get_value()

    def reset(self):
        self.hand.clear()
        self.aces = 0
        self.higher_score = 0
        self.lower_score = 0


class Dealer(Player):
    def __init__(self):
        super().__init__()


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

        self.player.take_card(self.deck_of_card.deal_card())

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
