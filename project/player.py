from hand import Hand
from data import Data


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.mistakes = 0
        self.plays = 0
        self.sim = False

    def set_hand(self, hand):
        self.hand = hand

    def hand_to_string(self):
        out = ''
        out += self.name
        out += ': Hand: '
        out += str(self.hand)
        out += ': Plays : '
        return out

    def play(self, trump, lead):
        # todo get input
        if self.sim:
            for card in self.hand:
                cards_in_hand = list(self.hand)
                card_to_play = card
                cards_in_hand.remove(card_to_play)
                play = Hand(card_to_play, cards_in_hand, lead, trump)
                if play.is_valid():
                    output = self.hand_to_string()
                    print output + card
                    self.hand.remove(card)
                    return card
        else:
            # todo capture user input
            valid = False
            choice = ''
            output = self.hand_to_string()
            while not valid:
                choice = raw_input(output)
                if choice in self.hand:
                    cards_in_hand = list(self.hand)
                    cards_in_hand.remove(choice)
                    valid = Hand(choice, cards_in_hand, lead, trump).is_valid()

            self.hand.remove(choice)
            return choice

    def set_simulate(self):
        self.sim = True

    def get_stats(self):
        return ''


class AIPlayer(Player):
    def __init__(self, name, classifier):
        Player.__init__(self, name)
        self.classifier = classifier

    def play(self, trump, lead):
        # todo implement classification check
        plays = []
        guess_valid = []
        guess_invalid = []
        for card in self.hand:
            cards_in_hand = list(self.hand)
            card_to_play = card
            cards_in_hand.remove(card_to_play)
            plays.append(Hand(card_to_play, cards_in_hand, lead, trump))

        # Run the plays through machine learning
        for play in plays:
            binary_play = play.to_binary_list()

            # 0 is valid, 1 is invalid
            best_guess, best_confidence = self.classifier.evaluate(Data(len(binary_play), data=binary_play))
            if best_guess == 0:
                guess_valid.append((play, best_confidence, play.is_valid()))
            else:
                guess_invalid.append((play, best_confidence, play.is_valid()))

        # Sort the guess list by most confident (valid) and least confident (invalid)
        guess_valid.sort(key=lambda x: x[1], reverse=True)
        guess_invalid.sort(key=lambda x: x[1])

        # We will get a valid play
        self.plays += 1
        output = self.hand_to_string()
        # Most confident first
        for valid in guess_valid:
            if valid[2]:
                print output + valid[0].play
                self.hand.remove(valid[0].play)
                return valid[0].play
            else:
                self.mistakes += 1

        # least confident mistake first
        for invalid in guess_invalid:
            if invalid[2]:
                print output + invalid[0].play
                self.hand.remove(invalid[0].play)
                return invalid[0].play
            else:
                self.mistakes += 1

        return None

    def set_simulate(self):
        pass

    def get_stats(self):
        accuracy = 1.0 - (float(self.mistakes) / self.plays)
        return "Mistakes Made: " + str(self.mistakes) + ' Overall Accuracy: ' + str(accuracy)
