import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routes import gameDict

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_games():
    gameDict.clear()
    yield
    gameDict.clear()


def start_game(**params):
    response = client.post("/api/tictactoe/start", params=params)
    assert response.status_code == 200
    return response.json()


###########################
## Basic routes
###########################

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_example_route():
    response = client.get("/api/example")
    assert response.status_code == 200
    assert response.json() == {"message": "This is an example route"}


###########################
## /api/tictactoe/start
###########################

def test_start_defaults():
    data = start_game()
    assert 1000 <= data["key"] <= 9999
    assert data["board"] == [""] * 9
    assert data["current_player"] == "X"
    assert data["winner"] is None
    assert data["moves"] == 0


def test_start_custom_params():
    data = start_game(ai_player="O", opponent_player="X", starting_player="O", difficulty="hard")
    assert data["current_player"] == "O"
    assert data["winner"] is None


def test_start_invalid_player_param():
    response = client.post("/api/tictactoe/start", params={"ai_player": "Z"})
    assert response.status_code == 422


def test_start_invalid_difficulty_param():
    response = client.post("/api/tictactoe/start", params={"difficulty": "extreme"})
    assert response.status_code == 422


###########################
## /api/tictactoe/state
###########################

def test_state_valid_key():
    started = start_game()
    response = client.get("/api/tictactoe/state", params={"key": started["key"]})
    assert response.status_code == 200
    assert response.json() == {
        "board": started["board"],
        "current_player": started["current_player"],
        "winner": started["winner"],
        "moves": started["moves"],
    }


def test_state_unknown_key():
    response = client.get("/api/tictactoe/state", params={"key": 1234})
    assert response.status_code == 404
    assert response.json() == {"error": "Game not found"}


def test_state_key_out_of_range():
    response = client.get("/api/tictactoe/state", params={"key": 500})
    assert response.status_code == 422


###########################
## /api/tictactoe/move
###########################

def test_move_valid():
    started = start_game(starting_player="X")
    key = started["key"]
    response = client.patch("/api/tictactoe/move", params={"key": key, "position": 0})
    assert response.status_code == 200
    data = response.json()
    assert data["board"][0] == "X"
    assert data["current_player"] == "O"
    assert data["moves"] == 1


def test_move_occupied_cell_is_invalid():
    started = start_game(starting_player="X")
    key = started["key"]
    client.patch("/api/tictactoe/move", params={"key": key, "position": 0})
    response = client.patch("/api/tictactoe/move", params={"key": key, "position": 0})
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid move"}


def test_move_unknown_key():
    response = client.patch("/api/tictactoe/move", params={"key": 1234, "position": 0})
    assert response.status_code == 404


def test_move_position_out_of_range():
    started = start_game()
    response = client.patch(
        "/api/tictactoe/move", params={"key": started["key"], "position": 9}
    )
    assert response.status_code == 422


def test_move_win_sequence():
    started = start_game(starting_player="X")
    key = started["key"]
    # X: 0, O: 3, X: 1, O: 4, X: 2 -> X completes the top row
    for position in [0, 3, 1, 4, 2]:
        response = client.patch(
            "/api/tictactoe/move", params={"key": key, "position": position}
        )
        assert response.status_code == 200
    data = response.json()
    assert data["winner"] == "X"

    # Further moves are rejected once the game is over
    response = client.patch("/api/tictactoe/move", params={"key": key, "position": 5})
    assert response.status_code == 400


def test_move_draw_sequence():
    started = start_game(starting_player="X")
    key = started["key"]
    # Alternating moves that fill the board with no winner:
    # X O X
    # X O O
    # O X X
    for position in [0, 1, 2, 4, 3, 5, 7, 6, 8]:
        response = client.patch(
            "/api/tictactoe/move", params={"key": key, "position": position}
        )
        assert response.status_code == 200
    data = response.json()
    assert data["winner"] == "Draw"
    assert data["moves"] == 9
    assert "" not in data["board"]


###########################
## /api/tictactoe/ai-move
###########################

def test_ai_move():
    started = start_game(ai_player="X", opponent_player="O", starting_player="X")
    key = started["key"]
    response = client.patch("/api/tictactoe/ai-move", params={"key": key})
    assert response.status_code == 200
    data = response.json()
    assert 0 <= data["move"] <= 8
    assert data["board"][data["move"]] == "X"
    assert data["moves"] == 1


def test_ai_move_unknown_key():
    response = client.patch("/api/tictactoe/ai-move", params={"key": 1234})
    assert response.status_code == 404


###########################
## /api/tictactoe/reset
###########################

def test_reset():
    started = start_game(starting_player="X")
    key = started["key"]
    client.patch("/api/tictactoe/move", params={"key": key, "position": 0})

    response = client.patch("/api/tictactoe/reset", params={"key": key})
    assert response.status_code == 200
    data = response.json()
    assert data["board"] == [""] * 9
    assert data["winner"] is None
    assert data["moves"] == 0


def test_reset_unknown_key():
    response = client.patch("/api/tictactoe/reset", params={"key": 1234})
    assert response.status_code == 404
