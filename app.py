from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    board = game.board

    info = {"game_id": game_id, "board": board}

    return jsonify(info)


@app.post("/api/score-word")
def score_word():
    """ should check if the word is legal, and return JSON """
    word = request.json.get("word")
    game_id = request.json.get("game_id")
    game = games[game_id]

    result = { "result" : "ok"}

    # if BoggleGame.is_word_in_word_list(word) and BoggleGame.check_word_on_board(word):
    #     result = { "result" : "ok"}

    if not game.is_word_in_word_list(word):
        result = { "result" : "not-word"}
    elif not game.check_word_on_board(word):
        result = { "result" : "not-on-board"}

    return jsonify(result)
