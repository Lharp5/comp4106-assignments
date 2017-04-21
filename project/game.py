from player import Player
from deck import Deck
import random


def get_value(card):
    if card == '9':
        return 1
    if card == '10':
        return 2
    if card == 'J':
        return 3
    if card == 'Q':
        return 4
    if card == 'K':
        return 5
    if card == 'A':
        return 6


def generate_trump():
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

    return trump


def sister_suit(trump, suit):
    return (trump == 'H' and suit == 'D') \
           or (trump == 'D' and suit == 'H') \
           or (trump == 'S' and suit == 'C') \
           or (trump == 'C' and suit == 'S')


class Game(object):
    def __init__(self, players):
        self.players = players
        self.scores = [0, 0]
        self.round_scores = [0, 0]

    def setup(self):
        print "Welcome to Machine Learning Euchre"
        print "Using Classification based Machine Learning"
        print "Some Changes to Rules:"
        print "Trump is assigned randomly and there is no bidding"
        print "Because there is no bidding, no Euchre points will be rewarded"

        choice = raw_input('Would you like to Simulate this game? (y/n)')
        if choice == 'y':
            for player in self.players:
                player.set_simulate()

    def declare_winner(self, trump, plays):
        lead_suit = plays[0][1][0]
        scores = []
        for player, play in plays:
            suit = play[0]
            card = play[1:]
            score = get_value(card)
            if suit != lead_suit and suit != trump:
                score = 0

            if suit == trump and card == 'J':
                score = 20
            elif card == 'J' and sister_suit(trump, suit):
                score = 30
            elif suit == trump:
                score += 10
            scores.append((player, score))

        best_score = -1
        winner = -1

        # Determine what card one
        for player, score in scores:
            if score > best_score:
                best_score = score
                winner = player

        if winner % 2 == 0:
            self.round_scores[0] += 1
        else:
            self.round_scores[1] += 1

        return winner

    def run(self):
        leader = 0
        while self.scores[0] != 10 and self.scores[1] != 10:
            print "======================="
            print "Round Start ::: Score: " + str(self.scores)
            print

            deck = Deck()

            # Deal the player their hand
            for player in self.players:
                hand = []
                for i in range(5):
                    hand.append(deck.deal_card())

                player.set_hand(hand)

            # Get Trump for this round
            trump = generate_trump()
            print "Trump is : " + trump
            current = leader
            self.round_scores = [0, 0]
            # Conduct a round
            for trick in range(5):
                plays = list()
                plays.append((current, self.players[current].play(trump, None)))
                # plays.append((current, 'H10'))
                current = (current + 1) % len(self.players)
                # iterate over the next players
                for next_player in range(3):
                    plays.append((current, self.players[current].play(trump, plays[0][1])))
                    # plays.append((current, 'SA'))
                    current = (current + 1) % len(self.players)

                current = self.declare_winner(trump, plays)
                print self.players[current].name + " Wins The Trick"
                print
            # todo: Add a display for the winning team, and the update to the current score
            if self.round_scores[0] > self.round_scores[1]:
                self.scores[0] += 1
            else:
                self.scores[1] += 1

            leader = (leader + 1) % len(self.players)

    def end(self):
        if self.scores[0] == 10:
            winners = [self.players[0], self.players[2]]
        else:
            winners = [self.players[1], self.players[3]]

        print 'Final Score: ' + str(self.scores)
        print winners[0].name + ' and ' + winners[1].name + ' Win!!!'

        print 'Final Stats:'
        for player in self.players:
            print player.name + ': ' + player.get_stats()
