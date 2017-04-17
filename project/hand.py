def binary_suit(suit):
    if suit == 'H':
        return '1000'

    if suit == 'S':
        return '0100'

    if suit == 'D':
        return '0010'

    if suit == 'C':
        return '0001'

    return '0000'


def binary_card(card):
    binary = ''

    if card is None:
        return '00000'

    if card[1] == 'J':
        binary += '1'
    else:
        binary += '0'

    binary += binary_suit(card[0])

    return binary


class Hand(object):
    def __init__(self, play, hand, lead, trump):
        self.play = play
        self.hand = hand
        self.lead = lead
        self.trump = trump

    # FORMAT OF BINARY: TRUMP, LEAD, PLAYED, HAND
    # For Each Card 5 Numbers: Jack, Heart, Spade, Diamond, Club
    def to_binary(self):
        binary_hand = ""
        binary_hand += binary_suit(self.trump)
        binary_hand += binary_card(self.lead)
        binary_hand += binary_card(self.play)
        for idx in range(4):  # We have at most 4 other cards in our hand
            if idx < len(self.hand):
                card = self.hand[idx]
            else:
                card = None
            binary_hand += binary_card(card)

        return binary_hand

    def from_binary(self):
        pass

    def left_bower(self, card):
        suit = card[0]

        if card[1] == 'J':
            if self.trump == 'H':
                return suit == 'D'
            if self.trump == 'D':
                return suit == 'H'
            if self.trump == 'S':
                return suit == 'C'
            if self.trump == 'C':
                return suit == 'S'
        else:
            return False

    def has_suit(self, suit):
        for card in self.hand:
            if card[0] == suit:
                return True

        return False

    def is_valid(self):
        # If leading, automatic success
        if self.lead is None:
            return True

        play_suit = self.play[0]
        lead_suit = self.lead[0]

        # Left Bower Lead cases
        if self.left_bower(self.lead) and play_suit != self.trump and self.has_suit(self.trump):
            return False

        # Left Bower played case:
        if self.left_bower(self.play) and lead_suit != self.trump and self.has_suit(lead_suit):
            return False

        # Check if not following suit
        if play_suit != lead_suit and self.has_suit(lead_suit):
            return False

        return True
