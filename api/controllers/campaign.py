from flask import Blueprint
from flask.views import MethodView

from services.utils import format_response

# Create a Blueprint for campaign-related routes
campaign_bp = Blueprint("campaigns", __name__)

class CampaignAPI(MethodView):
    def get(self):
        active_campaigns = [{
            "game": "mygame",
            "name": "mycampaign12",
            "priority": 10.5,
            "matchers": {
                "level": {
                    "min": 1,
                    "max": 5
                },
                "has": {
                    "country": [
                        "US",
                        "RO",
                        "CA"
                    ],
                    "items": [
                        "item_1"
                    ]
                },
                "does_not_have": {
                    "items": [
                        "item_4"
                    ]
                },
            },
            "start_date": "2022-01-25 00:00:00Z",
            "end_date": "2022-02-25 00:00:00Z",
            "enabled": True,
            "last_updated": "2021-07-13 11:46:58Z"
        }]
        return format_response({
            "active_campaigns": active_campaigns
        }, 200)

# Register the class-based view with a URL
campaign_bp.add_url_rule(
    "/active_campaigns",
    view_func=CampaignAPI.as_view("campaign_api"),
    methods=["GET"]
)
