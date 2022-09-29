from src.models import Card, Table


def run():
    table = Table()
    j1 = table.generate_player_deck("j1")
    j2 = table.generate_player_deck("j2")

    print(table.start_game())

    win = False

    while not win:
        turn = table.turn
        print("\n", turn)
        print("Top: ", table.top_card)
        print("Deck: ", table.player_decks[turn])
        op = "y"
        while op == "y":
            op = input("Steal a card? (y/n): ")
            if op.lower() == "y":
                table.steal(turn)
                print("Top: ", table.top_card)
                print("Deck: ", table.player_decks[turn])
        color = input("Color: ")
        number = input("Number: ")
        card = Card(color, number)
        try:
            win = table.put_card(turn, card)
            if win:
                break
            if card == Card("comodin", "+4"):
                new_color = input("New color: ")
                table.change_color(new_color)
            table.turn = table.next_player()
        except Exception as err:
            print(err)

    print("Player ", table.turn, " won!")


if __name__ == "__main__":
    run()
