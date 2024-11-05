from datetime import datetime

from flask import Blueprint
from flask import \
    current_app as app  # Import current_app to access the app context
from flask.views import MethodView
from marshmallow import ValidationError

from controllers.campaign import CampaignAPI
from schemas.player import PlayerSchema
from services.campaign import is_valid_campaign
from services.utils import format_response

# Create a Blueprint for player-related routes
player_bp = Blueprint("players", __name__)

class PlayerAPI(MethodView):
    schema = PlayerSchema()
    campaign_api = CampaignAPI()

    def get(self, player_id):
        # Get player from database
        player = app.dynamodb.get_item_by_id("players", {"player_id": player_id})
        if not player:
            return format_response("Failed to query dynamodb", 500)
        if not player.get("Item"):
            return format_response("Player not found in database", 404)

        # Validate player format
        try:
            player_data = self.schema.load(player["Item"])
        except ValidationError as err:
            return format_response(f"Validation error: {err.messages}", 422)
        app.logger.debug("Player: %s", player_data)

        # Get campaign
        campaigns, status_code = self.campaign_api.get()
        if status_code != 200:
            return format_response("Campaign not found", 404)

        # Check if campaign is valid
        updated = False
        for campaign in campaigns.json["active_campaigns"]:
            #TODO: confirm campaign names are unique
            if campaign["name"] in player_data["active_campaigns"]:
                continue
            if is_valid_campaign(campaign, player_data):
                app.logger.info("%s is valid", campaign["name"])
                player_data["active_campaigns"].append(campaign["name"])
                updated = True

        # Update player in db if needed
        if updated:
            player_data["modified"] = datetime.now()
            player_data = app.dynamodb.save_item("players", self.schema.dump(player_data))

        return format_response(player_data, 200)

# Register the class-based view with a URL
player_bp.add_url_rule(
    "/get_client_config/<player_id>",
    view_func=PlayerAPI.as_view("player_api"),
    methods=["GET"]
)
