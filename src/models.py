from typing import List
from typing import Dict
import random


class Card:
    def __init__(self, color: str, number: str):
        self.color = color
        self.number = number

    def __eq__(self, other) -> bool:
        return (self.color == other.color) or (self.number == other.number)

    def __repr__(self) -> str:
        return f'({self.color}, {self.number})'

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


baraja = [
    ('Rojo', '3'), ('Verde', '7'), ('Azul', '9'), ('Azul', '7'),
    ('Verde', '1'), ('Verde', '4'), ('Rojo', '5'), ('Rojo', '6'),
    ('Azul', '5'), ('Azul', '6'), ('Amarillo', '7'), ('Azul', '1'),
    ('Rojo', '1'), ('Verde', '6'), ('Amarillo', '3'), ('Amarillo', '0'),
    ('Verde', '2'), ('Verde', '3'), ('Verde', '9'), ('Rojo', '8'),
    ('Azul', '4'), ('Azul', '3'), ('Amarillo', '1'), ('Amarillo', '8'),
    ('Verde', '0'), ('Comodin', '+4'), ('Verde', '8'), ('Amarillo', '9'),
    ('Azul', '8'), ('Amarillo', '2'), ('Amarillo', '4'), ('Rojo', '9'),
    ('Rojo', '4'), ('Verde', '5'), ('Azul', '2'), ('Amarillo', '6'),
    ('Comodin', '+4'), ('Rojo', '0'), ('Amarillo', '5'), ('Azul', '0'),
    ('Rojo', '2'), ('Rojo', '7'), ('Amarillo', '+2'), ('Amarillo', '+2'),
    ('Amarillo', '+2'), ('Amarillo', '+2'), ('Verde', '+2'), ('Comodin', '+4'),
    ('Verde', '+2'), ('Verde', '+2'), ('Verde', '+2'), ('Comodin', '+4'),
    ('Azul', '+2'), ('Azul', '+2'), ('Azul', '+2'), ('Azul', '+2'),
    ('Rojo', '+2'), ('Rojo', '+2'), ('Rojo', '+2'), ('Rojo', '+2')
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

    def put_card(self, player: str, card: Card) -> bool:
        self.turn = player

        if card not in self.player_decks[player]:
            raise Exception(message="Card is not in player deck")

        if self.top_card != card:
            raise Exception(message="Move not allowed")

        index = self.player_decks[player].index(card)
        del self.player_decks[player][index]
        self.deck.append(self.top_card)
        self.suffle()
        self.top_card = card

        return len(self.player_decks[player]) == 1

    def next_player(self) -> str:
        players = self.player_decks.keys()
        current_index = players.index(self.turn)

        if current_index == len(players) - 1 and self.direction > 0:
            return players[0]

        return players[current_index + (1 * self.direction)]
