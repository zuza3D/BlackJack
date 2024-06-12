from game.card import CardRank, card_values

Action = {
    'H': 'hit',
    'S': 'stand',
    'D': 'double',
    'P': 'split'
}


class BasicStrategy:
    def __init__(self):
        self.strategy_table = self.create_strategy_table()

    def create_strategy_table(self):
        with open('game/basic_strategy.csv', 'r') as file:
            decision_table = {}
            dealer_cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"]
            for line in file:
                line = line.strip()
                split_line = line.split(";")
                player_cards = split_line[0]
                actions = split_line[1:]
                for idx in range(len(dealer_cards)):
                    decision_table[(player_cards, dealer_cards[idx])] = Action[actions[idx]]
        return decision_table

    def are_cards_equal(self, player_hand):
        return True if player_hand[0].get_rank() == player_hand[1].get_rank() else False

    def contains_ace(self, player_hand):
        return True if player_hand[0].get_rank() == CardRank.Ace or player_hand[1].get_rank() == CardRank.Ace else False

    def get_action(self, player_hand, dealer_card):
        dealer_card = str(card_values[dealer_card.get_rank()]) if dealer_card.get_rank() != CardRank.Ace else 'A'
        if self.contains_ace(player_hand):
            player_hand = ['A' if card.get_rank() == CardRank.Ace else str(card_values[card.get_rank()]) for card in player_hand]
            player_hand = sorted(player_hand)
            player_hand.reverse()
            return self.strategy_table[('-'.join(player_hand), dealer_card)]
        if self.are_cards_equal(player_hand):
            player_hand = [str(card_values[card.get_rank()]) for card in player_hand]
            return self.strategy_table[('-'.join(player_hand), dealer_card)]
        player_hand_score = sum([card_values[card.get_rank()] for card in player_hand])
        return self.strategy_table[(str(player_hand_score), dealer_card)]
