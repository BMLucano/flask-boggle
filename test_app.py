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

