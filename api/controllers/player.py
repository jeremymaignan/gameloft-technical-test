from datetime import datetime

from flask import Blueprint
from flask import \
    current_app as app  # Import current_app to access the app context
from flask import jsonify
from flask.views import MethodView
from marshmallow import ValidationError

from controllers.campaign import CampaignAPI
from schemas.player import PlayerSchema
from services.campaign import is_valid_campaign

# Create a Blueprint for player-related routes
player_bp = Blueprint('players', __name__)

class PlayerAPI(MethodView):
    schema = PlayerSchema()

    def get(self, player_id):
        # Get player from database
        player = app.dynamodb.get_item_by_id(player_id)
        if not player:
            return jsonify({'error': 'Player not found'}), 404

        try:
            player_data = self.schema.load(player)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 500
        app.logger.debug("Player: {}".format(player_data))

        # Get campaign
        campaign_api = CampaignAPI()
        campaigns, status_code = campaign_api.get()
        if status_code != 200:
            return jsonify({'error': 'Campaign not found'}), 404
        app.logger.debug("Active campaigns: {}".format(campaigns.json))

        # Check if campaign is valid
        number_campaigns = len(player_data["active_campaigns"])
        for campaign in campaigns.json["active_campaigns"]:
            app.logger.info("{} is valid: {}".format(campaign["name"], is_valid_campaign(campaign, player_data)))
            #TODO: confirm campaign names are unique
            if campaign["name"] not in player_data["active_campaigns"]:
                player_data["active_campaigns"].append(campaign["name"])

        if len(player["active_campaigns"]) != number_campaigns:
            player_data["modified"] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
            app.dynamodb.save_items(player_data)

        return jsonify(player_data), 200

# Register the class-based view with a URL
player_bp.add_url_rule(
    '/get_client_config/<player_id>',
    view_func=PlayerAPI.as_view('player_api'),
    methods=['GET']
)
