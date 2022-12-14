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

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')

            # test that you're getting a template
            html = response.get_data(as_text=True)
            self.assertIn('<!-- BOGGLE: FOR TEST PURPOSES -->', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:

            response = client.post('/api/new-game')
            json = response.get_json()

            # assertIsInstance
            self.assertTrue(type(json["game_id"]) == str)
            self.assertTrue(type(json["board"]) == list)
            self.assertIn(json["game_id"], games)
            ...
            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # test that the game_id is a string
            # test that the board is a list
            # test that the game_id is in the dictionary of games (imported from app.py above)

    def test_score_word(self):
        """Test if word is valid"""

        with self.client as client:

            response = client.post('/api/new-game')
            json = response.get_json()
            game_id = json["game_id"]
            game = games[game_id]

            # WHY NOT OVERWRITING?
            # breakpoint()
            # for row in game.board:
            #     row = ["C", "A", "T", "S", "S"]
            # breakpoint()

            game.board = [
                ["C", "A", "T", "S", "S"],
                ["C", "A", "T", "S", "S"],
                ["C", "A", "T", "S", "S"],
                ["C", "A", "T", "S", "S"],
                ["C", "A", "T", "S", "S"]
            ]


            resp_ok = client.post("/api/score-word",
                json={"game_id": game_id, "word": "CAT"})
            resp_not_word = client.post("/api/score-word",
                json={"game_id": game_id, "word": "CATSS"})
            resp_not_on_board = client.post("/api/score-word",
                json={"game_id": game_id, "word": "ABBEYS"})

            data_ok = resp_ok.get_json()
            data_not_word = resp_not_word.get_json()
            data_not_on_board = resp_not_on_board.get_json()

            self.assertEqual({ 'result' : 'ok'}, data_ok)
            self.assertEqual({ 'result' : 'not-word'}, data_not_word)
            self.assertEqual({ 'result' : 'not-on-board'}, data_not_on_board)





            ...
            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # find that game in the dictionary of games (imported from app.py above)

            # manually change the game board's rows so they are not random

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            # test to see that an invalid word returns {'result': 'not-word'}
