from uno_server.src.models.table import Table
from uno_server.src.models.card import Card


def run():
    table = Table()
    j1 = table.generate_player_deck("j1")
    j2 = table.generate_player_deck("j2")
    j3 = table.generate_player_deck("j3")

    print(table.start_game())

    win = False

    while not win:
        turn = table.turn
        print("Top: ", table.top_card)
        print("Deck: ", table.player_decks[turn])
        color = input("Color: ")
        number = input("Number: ")
        try:
            win = table.put_card(turn, Card(color, number))
            if win:
                break
            table.turn = table.next_player()
        except Exception as err:
            print(err)

    print("Player ", table.turn, " won!")


if __name__ == "__main__":
    run()
