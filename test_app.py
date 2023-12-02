from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            # test that you're getting a template, both <form id='newWordForm'>
            # and <table class="board"> will work
            # self.assertIn('<!-- homepage -->', html)  # will also work

            self.assertIn('<table class="board', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            response = client.post("/api/new-game")
            # print(response, "printing response")
            # breakpoint()
            payload = response.get_json()
            # print(payload, "printing payload")

            game_id = payload["game_id"]
            board = payload["board"]
            # breakpoint()
            # print(game_id, board)

            self.assertIn(game_id, games)
            self.assertTrue(board)

    def test_api_score_word(self):
        """Test scoring a word"""

        with app.test_client() as client:
            game = client.post("/api/new-game").get_json()
            # breakpoint()
            # print(game, "prinitng response")
            game_id = game["game_id"]
            game = games[game_id]

            # breakpoint()
            # print(game_id, "printing game id")
            # print(game.board, "printing board")

            # Changes the source of truth games (from app.py)
            # change what the letters are on the board before you try to score
            # the play

            game.board[0] = ["K", "H", "N", "E", "O"]
            game.board[1] = ["L", "C", "G", "G", "I"]
            game.board[2] = ["R", "Y", "D", "A", "M"]
            game.board[3] = ["I", "I", "E", "M", "K"]
            game.board[4] = ["Y", "F", "J", "L", "L"]
            # breakpoint()
            # print(game.board, "printing board after reassignment")
            # print(game_id, "printing game_id after reassignment")

            # Send a valid word to the score-word enpoint as JSON
            resp = client.post('/api/score-word',
                               json={'word': 'GAME', 'game_id': game_id})
            data = resp.get_json()

            self.assertEqual({'result': 'ok'}, data)

            # Send a valid but lowercase word to the score-word endpoint as JSON
            # FIXME: MIGHT FAIL
            resp = client.post('/api/score-word',
                               json={'word': 'game', 'game_id': game_id})
            data = resp.get_json()

            self.assertEqual({'result': 'ok'}, data)

            # Send a word not on the board to score-word endpoint as JSON
            resp = client.post('api/score-word',
                               json={'word': 'SCHOOL', 'game_id': game_id})
            data = resp.get_json()

            self.assertEqual({'result': 'not-on-board'}, data)

            # Send a gibberish word to score-word enpoint as JSON
            resp = client.post('api/score-word',
                               json={'word': 'THIFHDCK', 'game_id': game_id})
            data = resp.get_json()

            self.assertEqual({'result': 'not-word'}, data)
