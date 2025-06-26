from flask import Blueprint, jsonify, request
from .ticTacToe import TicTacToe

routes = Blueprint('routes', __name__)

@routes.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@routes.route('/api/example', methods=['GET'])
def example_route():
    return jsonify({'message': 'This is an example route'}), 200

###################################
## Routes for a tic-tac-toe game ##
###################################
# In-memory game instance (resets on server restart)
game = TicTacToe()

# get the current game state
# Returns the board, current player, winner, and number of moves made
@routes.route('/api/tictactoe/state', methods=['GET'])
def tictactoe_state():
    return jsonify(game.get_state()), 200

# Make a move on the board
# Expects a JSON body with the position (0-8) to place the current player's
# input format: {"position": 0}
@routes.route('/api/tictactoe/move', methods=['POST'])
def tictactoe_move():
    data = request.get_json()
    position = data.get("position")
    if position is None or not (0 <= position < 9):
        return jsonify({"error": "Invalid position"}), 400
    if game.make_move(position):
        return jsonify(game.get_state()), 200
    else:
        return jsonify({"error": "Invalid move"}), 400

# AI makes a move based on the current game state
@routes.route('/api/tictactoe/ai-move', methods=['POST'])
def tictactoe_ai_move():
    move = game.ai_move()
    return jsonify({"move": move, **game.get_state()}), 200

# Reset the game
@routes.route('/api/tictactoe/reset', methods=['POST'])
def tictactoe_reset():
    game.reset()
    return jsonify(game.get_state()), 200
