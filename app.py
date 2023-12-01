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


# Needs to send and receive JSON
@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify(game_id=game_id, board=game.board)

@app.post("/api/score-word")
def score_word():
    """Recieves JSON. Check if word is legal, score it and return JSON"""
    word = request.json["word"]
    game_id = request.json["game_id"]
    game = games[game_id]

    if not game.is_word_in_word_list(word):
        return jsonify(result = "not-word")
    if not game.check_word_on_board(word):
        return jsonify(result = "not-on-board")
    if game.is_word_not_a_dup(word):
        return jsonify(result = "ok")

