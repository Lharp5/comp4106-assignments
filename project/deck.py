import random

deck_of_cards = ['H9', 'H10', 'HJ', 'HQ', 'HK', 'HA',
                 'S9', 'S10', 'SJ', 'SQ', 'SK', 'SA',
                 'D9', 'D10', 'DJ', 'DQ', 'DK', 'DA',
                 'C9', 'C10', 'CJ', 'CQ', 'CK', 'CA',]


class Deck(object):
    def __init__(self):
        self.deck = list(deck_of_cards)
        random.seed()

    def deal_card(self):
        pos = random.randint(0, len(self.deck) - 1)
        ret = self.deck[pos]
        del self.deck[pos]
        return ret
