class InvalidCard(Exception):
    def __init__(
            self,
            message="Card is not in player deck."):
        self.message = message
        super().__init__(self.message)


class InvalidMove(Exception):
    def __init__(
            self,
            message="Move not allowed."):
        self.message = message
        super().__init__(self.message)
