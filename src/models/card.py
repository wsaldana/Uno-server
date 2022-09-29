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
