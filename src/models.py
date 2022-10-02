from typing import List
from typing import Dict
import random
import json
from json import JSONEncoder


from src.exceptions import InvalidCard, InvalidMove


class Card(dict):
    def __init__(self, color: str, number: str):
        self.color = color
        self.number = number
        dict.__init__(self, color=color, number=number)

    def __eq__(self, other) -> bool:
        return (self.color == other.color) or (self.number == other.number)

    def __str__(self) -> str:
        return json.dumps({
            'color': self.color,
            'number': self.number,
        })

    def __repr__(self) -> str:
        return str(self)

    def __dict__(self) -> dict:
        return {
            'color': self.color,
            'number': self.number,
        }


class Deck(list):
    def __init__(self, cards: List[Card] = [], *args) -> None:
        self.cards = cards
        list.__init__(self, *args)

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def pop(self):
        return self.cards.pop()

    def __setitem__(self, i, data):
        self.cards[i] = data

    def __getitem__(self, i):
        return self.cards[i]

    def __str__(self) -> str:
        return str([
            str(card) for card in self.cards
        ])

    def __repr__(self) -> str:
        return str(self)

    def index(self, card: Card):
        return self.cards.index(card)

    def __delitem__(self, key: index):
        del self.cards[key]

    def append(self, card: Card) -> None:
        self.cards.append(card)

    def __contains__(self, __o: Card) -> bool:
        for card in self.cards:
            if card.color == __o.color and card.number == __o.number:
                return True
        return False


baraja = [
    ('red', '3'), ('green', '7'), ('blue', '9'), ('blue', '7'),
    ('green', '1'), ('green', '4'), ('red', '5'), ('red', '6'),
    ('blue', '5'), ('blue', '6'), ('yellow', '7'), ('blue', '1'),
    ('red', '1'), ('green', '6'), ('yellow', '3'), ('yellow', '0'),
    ('green', '2'), ('green', '3'), ('green', '9'), ('red', '8'),
    ('blue', '4'), ('blue', '3'), ('yellow', '1'), ('yellow', '8'),
    ('green', '0'), ('black', '+4'), ('green', '8'), ('yellow', '9'),
    ('blue', '8'), ('yellow', '2'), ('yellow', '4'), ('red', '9'),
    ('red', '4'), ('green', '5'), ('blue', '2'), ('yellow', '6'),
    ('black', '+4'), ('red', '0'), ('yellow', '5'), ('blue', '0'),
    ('red', '2'), ('red', '7'), ('yellow', '+2'), ('yellow', '+2'),
    ('yellow', '+2'), ('yellow', '+2'), ('green', '+2'), ('black', '+4'),
    ('green', '+2'), ('green', '+2'), ('green', '+2'), ('black', '+4'),
    ('blue', '+2'), ('blue', '+2'), ('blue', '+2'), ('blue', '+2'),
    ('red', '+2'), ('red', '+2'), ('red', '+2'), ('red', '+2')
]


class Table:
    def __init__(self) -> None:
        self.top_card: Card = None
        self.deck: Deck = []
        self.player_decks: Dict[str, Deck] = {}
        self.direction: int = 1
        self.turn: str = ""

        self.load_deck()
        self.shuffle()

    def load_deck(self) -> Deck:
        deck = [
            Card(i[0], i[1]) for i in baraja
        ]
        self.deck = Deck(deck)
        return self.deck

    def shuffle(self) -> None:
        random.shuffle(self.deck)

    def generate_player_deck(self, name: str) -> Deck:
        random_cards = [self.deck.pop() for _ in range(7)]
        new_deck = Deck(random_cards)
        self.player_decks[name] = new_deck

        if self.turn == "":
            self.turn = name
            self.start_game()

        return new_deck

    def start_game(self) -> Card:
        self.top_card = self.deck.pop()

    def change_color(self, color: str):
        self.top_card.color = color

    def put_card(self, player: str, card: Card, new_color: str = None) -> bool:
        self.turn = player

        if card not in self.player_decks[player]:
            if card.number != "+4":
                raise InvalidCard()

        if self.top_card.color != card.color and self.top_card.number != card.number:
            if card.number != "+4":
                raise InvalidMove()

        # Comodines
        if card == Card("black", "+4"):
            for _ in range(4):
                self.player_decks[self.next_player()].append(self.deck.pop())

        if card == Card("any", "+2"):
            for _ in range(2):
                self.player_decks[self.next_player()].append(self.deck.pop())

        index = self.player_decks[player].index(card)
        del self.player_decks[player][index]
        self.deck.append(self.top_card)
        self.shuffle()
        self.top_card = card

        return len(self.player_decks[player]) == 1

    def next_player(self) -> str:
        players = list(self.player_decks.keys())
        current_index = players.index(self.turn)

        if current_index == len(players) - 1 and self.direction > 0:
            return players[0]

        return players[current_index + (1 * self.direction)]

    def steal(self, player: str) -> Card:
        card = self.deck.pop()
        self.player_decks[player].append(card)
        return card
