from deck_of_card import DeckOfCard
from card import Card, CardRank


class Player:
    hand: list[Card]
    extra_point_ace: bool
    score: int

    def __init__(self):
        self.hand = list()
        self.extra_point_ace = False
        self.score = 0

    def take_card(self, card):
        self.hand.append(card)

        card_value = card.get_value()
        card_rank = card.get_rank()

        self.score += card_value
        if card_rank == CardRank.Ace and not self.extra_point_ace:
            self.extra_point_ace = True

    def reset(self):
        self.hand.clear()
        self.extra_point_ace = False
        self.score = 0

    def __str__(self):
        return (f'Player: {self.score} | {self.score+10}' if self.extra_point_ace
                else f'Player: {self.score}')

    def is_lost(self):
        return True if self.score > 21 else False

    def has_blackjack(self):
        return True if self.score == 21 or self.score + self.extra_point_ace * 10 == 21 else False


class Dealer(Player):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return (f'Dealer: {self.score} | {self.score + 10}' if self.extra_point_ace
                else f'Dealer: {self.score}')


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
        self.deck_of_card = DeckOfCard()
        self.deck_of_card.shuffle()
        self.deal_initial_cards()

    def deal_initial_cards(self):
        for i in range(2):
            self.dealer.take_card(self.deck_of_card.deal_card())
            self.player.take_card(self.deck_of_card.deal_card())

    def player_hit(self):
        self.player.take_card(self.deck_of_card.deal_card())

    def dealer_play(self):
        dealer_score = self.dealer.score
        while dealer_score + self.dealer.extra_point_ace * 10 < 17 and dealer_score < 17:
            self.dealer.take_card(self.deck_of_card.deal_card())
            dealer_score = self.dealer.score

    def find_winner(self):
        player_ace = self.player.extra_point_ace
        dealer_ace = self.dealer.extra_point_ace
        player_score = self.player.score + player_ace * 10
        dealer_score = self.dealer.score + dealer_ace * 10

        player_score = player_score if player_score <= 21 else player_score - player_ace * 10
        dealer_score = dealer_score if dealer_score <= 21 else dealer_score - dealer_ace * 10

        if player_score > 21:
            return f'Dealer wins'
        if dealer_score > 21:
            return f'Player wins'
        if player_score > dealer_score:
            return f'Player wins'
        if dealer_score > player_score:
            return f'Dealer wins'
        return "It's a tie!"

    def is_game_over(self):
        if self.player.is_lost() or self.player.has_blackjack():
            self.find_winner()
