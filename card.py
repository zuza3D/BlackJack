from enum import Enum


class CardSuit(Enum):
    spade = 1
    heart = 2
    diamonds = 3
    club = 4


class CardRank(Enum):
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13


card_values = {
    CardRank.Two: 2,
    CardRank.Three: 3,
    CardRank.Four: 4,
    CardRank.Five: 5,
    CardRank.Six: 6,
    CardRank.Seven: 7,
    CardRank.Eight: 8,
    CardRank.Nine: 9,
    CardRank.Ten: 10,
    CardRank.Jack: 10,
    CardRank.Queen: 10,
    CardRank.King: 10,
    CardRank.Ace: 11

}


class Card:
    _rank: CardRank
    _suit: CardSuit
    _value: int

    def __init__(self, rank, suit):
        self._rank = rank
        self._suit = suit
        self._value = card_values[rank]

    def __repr__(self):
        return f'{self._rank.name} of {self._suit.name} ({self._value} points)'

