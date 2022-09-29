from typing import List
from typing import Dict
import random

from src.exceptions import InvalidCard, InvalidMove


class Card:
    def __init__(self, color: str, number: str):
        self.color = color
        self.number = number

    def __eq__(self, other) -> bool:
        return (self.color == other.color) or (self.number == other.number)

    def __str__(self) -> str:
        return f'({self.color}, {self.number})'

    def __repr__(self) -> str:
        return str(self)

    def __dict__(self) -> dict:
        return {
            'color': self.color,
            'number': self.number,
        }


class Deck:
    def __init__(self, cards: List[Card] = []) -> None:
        self.cards = cards

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


baraja = [
    ('rojo', '3'), ('verde', '7'), ('azul', '9'), ('azul', '7'),
    ('verde', '1'), ('verde', '4'), ('rojo', '5'), ('rojo', '6'),
    ('azul', '5'), ('azul', '6'), ('amarillo', '7'), ('azul', '1'),
    ('rojo', '1'), ('verde', '6'), ('amarillo', '3'), ('amarillo', '0'),
    ('verde', '2'), ('verde', '3'), ('verde', '9'), ('rojo', '8'),
    ('azul', '4'), ('azul', '3'), ('amarillo', '1'), ('amarillo', '8'),
    ('verde', '0'), ('comodin', '+4'), ('verde', '8'), ('amarillo', '9'),
    ('azul', '8'), ('amarillo', '2'), ('amarillo', '4'), ('rojo', '9'),
    ('rojo', '4'), ('verde', '5'), ('azul', '2'), ('amarillo', '6'),
    ('comodin', '+4'), ('rojo', '0'), ('amarillo', '5'), ('azul', '0'),
    ('rojo', '2'), ('rojo', '7'), ('amarillo', '+2'), ('amarillo', '+2'),
    ('amarillo', '+2'), ('amarillo', '+2'), ('verde', '+2'), ('comodin', '+4'),
    ('verde', '+2'), ('verde', '+2'), ('verde', '+2'), ('comodin', '+4'),
    ('azul', '+2'), ('azul', '+2'), ('azul', '+2'), ('azul', '+2'),
    ('rojo', '+2'), ('rojo', '+2'), ('rojo', '+2'), ('rojo', '+2')
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

        return new_deck

    def start_game(self) -> Card:
        self.top_card = self.deck.pop()

    def change_color(self, color: str):
        self.top_card.color = color

    def put_card(self, player: str, card: Card, new_color: str = None) -> bool:
        self.turn = player

        if card not in self.player_decks[player]:
            raise InvalidCard()

        if self.top_card != card:
            if card != Card("comodin", "+4"):
                raise InvalidMove()

        # Comodines
        if card == Card("comodin", "+4"):
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
