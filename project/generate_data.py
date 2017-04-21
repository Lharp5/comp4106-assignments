from deck import Deck
from hand import Hand
import random

correct_file = 'correct_move.txt'
incorrect_file = 'incorrect_move.txt'


def write_entry(input_file, play):
        with open(input_file, 'a') as write_file:
            write_file.write(play.to_binary() + '\n')


def generate_data(num_data):
    num_left = num_data
    valid_plays = []
    invalid_plays = []
    while num_left > 0:
        for num_cards in range(1, 6):
            hand = []
            deck = Deck()
            for i in range(num_cards):
                hand.append(deck.deal_card())

            turn_to_lead = random.randint(1, 4)

            if turn_to_lead > 1:
                lead = deck.deal_card()
            else:
                lead = None

            trump_num = random.randint(1, 4)

            # 1 = H 2 = S 3 = D 4 = C
            if trump_num == 1:
                trump = 'H'
            elif trump_num == 2:
                trump = 'S'
            elif trump_num == 3:
                trump = 'D'
            else:
                trump = 'C'

            for card in hand:
                cards_in_hand = list(hand)
                card_to_play = card
                cards_in_hand.remove(card_to_play)
                play = Hand(card_to_play, cards_in_hand, lead, trump)

                if play.is_valid():
                    write_entry(correct_file, play)
                else:
                    write_entry(incorrect_file, play)
                num_left -= 1
