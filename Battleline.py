import random

print('Coding battleline!')


class Card():
    def __init__(self, istroop, color, value, tactics):
        '''
        :param istroop: True, False
        True represents troop cards, False represents tactics cards
        :param color: 'None', 'red', 'green', 'blue', 'yellow', 'purple', 'orange'
        The color of the card
        :param value: 'None', 1, 2, ..., 10
        The value of the card
        :param tactics: 'None', 'Alex', 'Darius', '8', '123', 'Fog', 'Mud', 'Star', 'Redeploy', 'Bridge', 'Goat'
        Names for the tactics cards, think about their possible Chinese translations

        state: 'deck', 'hand', 'city', 'discarded'
        Where is this card? In the deck? In players' hands? ...
        side: 'None', 'A', 'B'
        Which side is the card on? Side A or side B?
        city: 'None', '1', '2', ..., '9'
        Which city is the card at? City 1 or city 2 or ...
        '''

        self.istroop = istroop
        self.color = color
        self.value = value
        self.tactics = tactics

        self.state = 'deck'
        self.side = 'None'
        self.city = 'None'

    # https://lerner.co.il/2014/10/14/python-attributes/
    def __repr__(self):
        return repr((self.istroop, self.color, self.value, self.tactics))

    def change_color(self, new_color):
        self.color = new_color

    def change_value(self, new_value):
        self.value = new_value

    def change_state(self, new_state):
        self.state = new_state

    def change_side(self, new_side):
        self.side = new_side

    def change_city(self, new_city):
        self.city = new_city


class City():
    def __init__(self, city):
        '''
        :param city: '1', '2', ..., '9'
        This city is city No.1, No.2, ...

        cards_A: [card_A1, card_A2, card_A3], a list containing Card-class elements
        Cards on side A. No more than three
        cards_B: [same, with A -> B]
        Same, with A -> B

        fogmud_A: [fogmud_A1, fogmud_A2], a list containing a Card-class element
        Fogmud means fog and mud. This is for the environment cards on side A
        fogmud_B: [same, with A -> B]
        Same, with A -> B

        form_A: 'None', 'Wedge', 'Phalanx', 'Battalion', 'Skirmish', 'Host'
        The form formed by the cards on side A
        form_B: same
        Same, with A -> B

        sum_A: 0, 1, 2, ..., 30
        The sum of the values of the cards on side A
        sum_B: same
        Same, with A -> B

        side: 'None', 'A', 'B'
        Who owns the city? Player A or player B? Or still not decided?
        '''

        self.city = city

        self.cards_A = []
        self.cards_B = []
        self.fogmud_A = []
        self.fogmud_B = []

        self.form_A = 'None'
        self.form_B = 'None'
        self.sum_A = 0
        self.sum_B = 0

        self.side = 'None'

    def plus_card(self, card, side):
        card.state = 'city'
        card.side = side
        card.city = self.city
        if side == 'A':
            self.cards_A.append(card)
        else:
            self.cards_B.append(card)

    def minus_card(self, card, side):
        if side == 'A':
            self.cards_A.remove(card)
        else:
            self.cards_B.remove(card)

    def plus_fogmud(self, fogmud, side):
        fogmud.state = 'city'
        fogmud.side = side
        fogmud.city = self.city
        if side == 'A':
            self.cards_A.append(fogmud)
        else:
            self.cards_B.append(fogmud)

    def minus_fogmud(self, fogmud, side):
        if side == 'A':
            self.cards_A.remove(fogmud)
        else:
            self.cards_B.remove(fogmud)

    def judge_form(self):
        if len(self.cards_A) < 3:
            self.form_A = 'None'
        else:
            # https://docs.python.org/zh-cn/3/howto/sorting.html
            sorted_cards_A = sorted(self.cards_A, key=lambda card: card.value)

            color1, value1 = sorted_cards_A[0].color, sorted_cards_A[0].value
            color2, value2 = sorted_cards_A[1].color, sorted_cards_A[1].value
            color3, value3 = sorted_cards_A[2].color, sorted_cards_A[2].value

            self.sum_A = value1 + value2 + value3

            if color1 == color2 == color3 and value1 + 2 == value2 + 1 == value3:
                self.form_A = 'Wedge'
            elif value1 == value2 == value3:
                self.form_A = 'Phalanx'
            elif color1 == color2 == color3:
                self.form_A = 'Battalion'
            elif value1 + 2 == value2 + 1 == value3:
                self.form_A = 'Skirmish'
            else:
                self.form_A = 'Host'

        print("The form on side A is:", self.form_A, 'with value sum', self.sum_A)

        if len(self.cards_B) < 3:
            self.form_B = 'None'
        else:
            # https://docs.python.org/zh-cn/3/howto/sorting.html
            sorted_cards_B = sorted(self.cards_B, key=lambda card: card.value)

            color1, value1 = sorted_cards_B[0].color, sorted_cards_B[0].value
            color2, value2 = sorted_cards_B[1].color, sorted_cards_B[1].value
            color3, value3 = sorted_cards_B[2].color, sorted_cards_B[2].value

            self.sum_B = value1 + value2 + value3

            if color1 == color2 == color3 and value1 + 2 == value2 + 1 == value3:
                self.form_B = 'Wedge'
            elif value1 == value2 == value3:
                self.form_B = 'Phalanx'
            elif color1 == color2 == color3:
                self.form_B = 'Battalion'
            elif value1 + 2 == value2 + 1 == value3:
                self.form_B = 'Skirmish'
            else:
                self.form_B = 'Host'

        print("The form on side B is:", self.form_B, 'with value sum', self.sum_B)

    def captured(self, side):
        self.side = side


card1 = Card(True, 'red', 7, 'None')
card2 = Card(True, 'green', 8, 'None')
card3 = Card(True, 'blue', 9, 'None')
city = City(1)
city.plus_card(card1, 'A')
city.plus_card(card2, 'A')
city.plus_card(card3, 'A')
city.judge_form()


class Player():
    def __init__(self, side):
        '''
        :param side: 'A', 'B'
        Which side is the player on? Side A or side B?

        troop_cards: [card1, card2, ..., card7], a list containing Card-class elements
        Contains all the troop cards in the players hand
        tactics_cards: [card1, card2, ..., card7], a list containing Card-class elements
        Contains all the tactics cards in the players hand
        tactics_played: 0, 1, 2, 3, 4, 5
        The number of tactics cards the player has played. No more than five
        '''

        self.side = side

        self.troop_cards = []
        self.tactics_cards = []
        self.tactics_played = 0

    def plus_troop(self, card):
        card.state = 'hand'
        self.troop_cards.append(card)

    def plus_tactics(self, card):
        card.state = 'hand'
        self.tactics_cards.append(card)

    def minus_troop(self, card):
        self.troop_cards.remove(card)

    def minus_tactics(self, card):
        self.tactics_cards.remove(card)


class TroopDeck():
    def __init__(self):
        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.cards = []
        for color in colors:
            for value in values:
                self.cards.append(Card(True, color, value, 'None'))
        random.shuffle(self.cards)

    def minus_card(self):
        self.cards.pop()


class TacticsDeck():
    def __init__(self):
        names = ['Alex', 'Darius', '8', '123', 'Fog', 'Mud', 'Star', 'Redepoly', 'Bridge', 'Goat']
        self.cards = []
        for name in names:
            self.cards.append(Card(False, 'None', 'None', name))
        random.shuffle(self.cards)

    def minus_card(self):
        self.cards.pop()


deck = TroopDeck()
deck.minus_card()
print(deck.cards)
deck.minus_card()
print(deck.cards)
