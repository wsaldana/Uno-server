from typing import List

from uno_server.src.models.card import Card


class Deck:
    def __init__(self, cards: List[Card] = []) -> None:
        self.cards = cards

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def pop(self):
        return self.cards.pop()
