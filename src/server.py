import eventlet
import socketio
import json

from src.models import Table, Card


class Server:
    sio = socketio.Server(cors_allowed_origins='*')
    rooms = {}
    players_conn = {}

    def __init__(self) -> None:
        app = socketio.WSGIApp(Server.sio)
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

    @sio.event
    def connect(sid, environ):
        print('connect ', sid)

    @sio.event
    def message(sid, data):
        print('message ', data)
        json_message =  json.loads(data)
        Server.handle_messages(json_message, sid)

    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)

    @classmethod
    def handle_messages(self, msg_json: str, sid):
        if msg_json["query"] == "CREATE_ROOM":
            self.rooms[msg_json["room"]] = Table()
            self.sio.emit('message', {
                "message": "Done",
                "statusCode": 200,
                "query": "CREATE_ROOM",
            }, room=sid)

        elif msg_json["query"] == "ENTER_ROOM":
            try:
                table = self.rooms[msg_json["room"]]
                deck = table.generate_player_deck(msg_json["player"])
                self.players_conn[sid] = msg_json["player"]
                self.sio.emit('message', {
                    "message": "Done",
                    "statusCode": 200,
                    "playerDeck": deck,
                    "topCard": table.top_card,
                    "turn": table.turn,
                    "query": "ENTER_ROOM",
                }, room=sid)
            except Exception as err:
                print(err)
                self.sio.emit('message', {
                    "message": "Error creating room",
                    "statusCode": 400,
                    "query": "ENTER_ROOM",
                }, room=sid)

        elif msg_json["query"] == "PUT_CARD":
            try:
                table = self.rooms[msg_json["room"]]
                print(table.player_decks)
                win = table.put_card(
                    msg_json["player"],
                    Card(
                        msg_json["card"]["color"],
                        msg_json["card"]["number"]
                    ),
                )
                self.sio.emit('message', {
                    "message": "Done",
                    "statusCode": 200,
                    "query": "PUT_CARD",
                }, room=sid)

                if msg_json["card"]["color"] == "comodin":
                    table.change_color(msg_json["new_color"])
                table.turn = table.next_player()
                # self.broadcast_status(table, win)
            except Exception as err:
                print(err)
                self.sio.emit('message', {
                    "message": str(err),
                    "statusCode": 400,
                    "query": "PUT_CARD",
                }, room=sid)

        elif msg_json["query"] == "STEAL_CARD":
            try:
                table = self.rooms[msg_json["room"]]
                table.steal(msg_json["player"])
                self.sio.emit('message', {
                    "message": "Done",
                    "statusCode": 200,
                    "playerDeck": table.player_decks[
                        msg_json["player"]
                    ],
                    "query": "STEAL_CARD",
                }, room=sid)
            except Exception as err:
                print(err)
                self.sio.emit('message', {
                    "message": "Error puting card",
                    "statusCode": 400,
                    "query": "STEAL_CARD",
                }, room=sid)

        elif msg_json["query"] == "BROADCAST":
            table = self.rooms[msg_json["room"]]
            self.sio.emit('message', {
                "playerDeck": table.player_decks[msg_json["player"]],
                "topCard": table.top_card,
                "turn": table.turn,
                "query": "BROADCAST",
            }, room=sid)

        else:
            print(msg_json)

    @classmethod
    def broadcast_status(self, table, win):
        for player in self.players_conn.keys():
            self.sio.emit('message', {
                "playerDeck": table.player_decks[player],
                "topCard": table.top_card,
                "turn": table.turn,
                "win": "true" if win else "false",
                "query": "BROADCAST",
            }, room=player)


if __name__ == "__main__":
    socket = Server()
