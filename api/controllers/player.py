from flask import jsonify
from flask import Blueprint, jsonify
from flask.views import MethodView
from schemas.player import PlayerSchema
from flask import current_app  # Import current_app to access the app context
from marshmallow import ValidationError
import logging

# Create a Blueprint for user-related routes
player_bp = Blueprint('players', __name__)

class PlayerAPI(MethodView):
    schema = PlayerSchema()

    def get(self):

        # Handle GET request (e.g., return user list or user data)
        player_item = current_app.dynamodb.get_item_by_id("97983be2-98b7-11e7-90cf-082e5f28d836")
        print("okok")
        if player_item:
            print(f"Retrieved player item: {player_item}")
            try:
                # Ensure player_item is a dictionary that Marshmallow expects
                player_data = self.schema.load(data=player_item)  # Load and validate the data
                return jsonify(player_data), 200
            except ValidationError as err:
                return jsonify({'errors': err.messages}), 400
        else:
            return jsonify({'error': 'Player not found'}), 404

# Register the class-based view with a URL
player_bp.add_url_rule('/players', view_func=PlayerAPI.as_view('player_api'), methods=['GET', 'POST'])