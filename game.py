import gym
import random
from os import system, name

DECK = [
        'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS'
        'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH'
        'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC'
        'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD'
        ]

def card_value(card):
    assert(len(card) > 1)

    if card[0] in ['T', 'J', 'Q', 'K']:
        return 10
    elif card[0] == 'A':
        return 1
    else:
        return ord(card[0]) - ord('0')

def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

class Game(gym.Env):
    action_space = ['h', 's']

    def __init__(self):
        self.reset()

    def __get_state(self):
        if self.done:
            return [self.player_score, self.dealer_score, self.usable_ace]
        else:
            return [self.player_score, card_value(self.dealer[0]), self.usable_ace]

    def __deal(self, player=True):
        if player:
            hand = self.player
        else:
            hand = self.dealer

        card = self.deck[self.deck_index]
        self.deck_index+=1
        hand.append(card)

        score = 0
        ace = True
        usable_ace = False
        for card in hand:
            value = card_value(card)
            score += value

            if value == 1:
                usable_ace = True

        if ace and score <= 11:
            usable_ace = True
            score += 10

        if player:
            self.player_score = score
            self.usable_ace = usable_ace
        else:
            self.dealer_score = score

    def step(self, action):
        reward = 0
        if action == 's':
            self.done = True
            while self.dealer_score <= 17:
                self.__deal(player=False)

            self.done = True
            if self.dealer_score > 21 or (self.player_score <= 21 and self.player_score > self.dealer_score):
                reward = 1
            else:
                reward = -1

        elif action == 'h':
            self.__deal(player=True)

            if self.player_score > 21:
                reward = -1
                self.done = True
        else:
            print('action {} is not valid'.format(action))
            raise ValueError

        state = self.__get_state()
        return state, reward, self.done, dict()

    def reset(self):
        self.deck = DECK
        self.dealer = list()
        self.player = list()
        self.dealer_score = 0
        self.dealer_score = 0
        self.deck_index = 0
        self.done = False

        self.__deal(player=True)
        self.__deal(player=True)
        self.__deal(player=False)
        self.__deal(player=False)

    def render(self, mode='human'):
        string = ''
        if self.done:
            string += 'DEALER: {}\n'.format(self.dealer_score)
            for card in self.dealer:
                string += '{} '.format(card)
            string += '\n\n'

        else:
            string += 'DEALER: {}\n'.format(card_value(self.dealer[0]))
            string += '{} ?\n'.format(self.dealer[0])
            string += '\n'

        string += 'PLAYER: {}\n'.format(self.player_score)
        for card in self.player:
            string += '{} '.format(card)
        string += '\n\n'

        if self.done:
            if self.dealer_score > 21 or (self.player_score <= 21 and self.player_score > self.dealer_score):
                string += 'Player won!\n'
            else:
                string += 'Dealer won!\n'

        if mode == 'human':
            print(string)
        elif mode == 'ansi':
            return string
        else:
            raise NotImplementedError

    def close(self):
        return

    def seed(self, seed=None):
        self.seed = seed
        random.seed(seed)
        return seed
