from flask import Blueprint, jsonify

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
