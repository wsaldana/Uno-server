# Create new room
query = {
    "query": "CREATE_ROOM",
    "room": "xyz",
}
res = {
    "message": "Done || Error creating room",
    "statusCode": 200 or 400,
}


# Enter room
query = {
    "query": "ENTER_ROOM",
    "room": "xyz",
    "player": "player1",
}
res = {
    "message": "Done || Error entering room",
    "statusCode": 200 or 400,
    # "deck": [{"color": "aaa", "number": "1"}],
    "playerDeck": [{"color": "aaa", "number": "1"}],
    "topCard": {"color": "aaa", "number": "1"},
    "turn": "player1",
}

# Broadcast status
query = {
    "query": "BROADCAST",
    "room": "xyz",
    "player": "player1",
}
res = {
    "playerDeck": [{"color": "aaa", "number": "1"}],
    "topCard": {"color": "aaa", "number": "1"},
    "turn": "player1",
    "win": "true || false"
}

# Put card
query = {
    "query": "PUT CARD",
    "room": "xyz",
    "player": "player1",
    "card": {
        "color": "aaa",
        "number": "1",
    },
    "new_color": "aaa || None",
}
res = {
    "message": "Done || Error puting card",
    "statusCode": 200 or 400,
}

# Steal card
query = {
    "query": "STEAL CARD",
    "room": "xyz",
    "player": "player1",
}
res = {
    "message": "Done || Error stealing card",
    "statusCode": 200 or 400,
    "playerDeck": [{"color": "aaa", "number": "1"}],
}
