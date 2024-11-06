import copy
import logging
import unittest
from unittest.mock import MagicMock, patch

from flask import Flask

from controllers.player import \
    player_bp  # Make sure to import your player blueprint correctly


#pylint: disable=duplicate-code
class TestPlayerAPI(unittest.TestCase):
    player_id = "dbbbb135-02d7-4575-972e-b6d4a506fb0d"
    player_mock = {
        "Item": {
            "player_id": player_id,
            "credential": "sample_credential",
            "created": "2023-01-01 12:00:00Z",
            "modified": "2023-01-02 12:00:00Z",
            "last_session": "2023-01-02 13:00:00Z",
            "total_spent": 100,
            "total_refund": 10,
            "total_transactions": 5,
            "last_purchase": "2023-01-02 12:00:00Z",
            "active_campaigns": ["campaign_1"],
            "devices": [],
            "level": 3,
            "xp": 1500,
            "total_playtime": 1000,
            "country": "US",
            "language": "en",
            "birthdate": "1990-01-01 00:00:00Z",
            "gender": "male",
            "inventory": {
                "item_1": 5,
                "item_2": 3
            },
            "clan": {
                "id": "123456",
                "name": "Hello world clan"
            }
        }
    }
    campaign_mock = {
        "active_campaigns": [{
            "game": "game",
            "name": "campaign2",
            "priority": 10.5,
            "matchers": {
                "level": {
                    "min": 1,
                    "max": 10
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
    }

    def setUp(self):
        # Create a Flask app context for testing
        app = Flask(__name__)
        app.register_blueprint(player_bp)
        self.app = app.test_client()
        app.logger.setLevel(logging.CRITICAL)
        with app.app_context():
            # Attach the mock_dynamodb to the Flask app instance
            self.mock_dynamodb = MagicMock()
            app.dynamodb = self.mock_dynamodb

    def tearDown(self):
        self.mock_dynamodb.reset_mock()

    def test_fail_to_fetch_player_from_db(self):
        # With
        self.mock_dynamodb.get_item_by_id.return_value = None

        # When
        response = self.app.get(f'/get_client_config/{self.player_id}')

        # Assert
        self.assertEqual(response.status_code, 500)
        self.assertIn("Failed to query dynamodb", response.get_json()["message"])

    def test_player_not_found_in_db(self):
        # With
        self.mock_dynamodb.get_item_by_id.return_value = {"Item": []}

        # When
        response = self.app.get(f'/get_client_config/{self.player_id}')

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertIn("Player not found in database", response.get_json()["message"])

    def test_player_validation_error(self):
        # With
        invalid_player_mock = {"Item": {"player_id": self.player_id}}
        self.mock_dynamodb.get_item_by_id.return_value = invalid_player_mock

        # When
        response = self.app.get(f'/get_client_config/{self.player_id}')

        # Assert
        self.assertEqual(response.status_code, 422)
        self.assertIn("Validation error", response.get_json()["message"])

    @patch('controllers.player.CampaignAPI.get')
    def test_campaign_not_found(self, mock_get):
        # With
        self.mock_dynamodb.get_item_by_id.return_value = self.player_mock
        mock_get.return_value = (MagicMock(json={}), 404)

        # When
        response = self.app.get(f'/get_client_config/{self.player_id}')

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertIn("Campaign not found", response.get_json()["message"])

    @patch('controllers.player.CampaignAPI.get')
    def test_player_update_with_new_valid_campaign(self, mock_get):
        # With
        self.mock_dynamodb.get_item_by_id.return_value = self.player_mock
        self.mock_dynamodb.save_item.return_value = True
        mock_response = MagicMock()
        mock_response.json = self.campaign_mock
        mock_get.return_value = (mock_response, 200)

        # When
        response = self.app.get(f'/get_client_config/{self.player_id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertIn("campaign2", response_json["active_campaigns"])
        self.mock_dynamodb.save_item.assert_called_once_with("players", response_json)

    @patch('controllers.player.CampaignAPI.get')
    def test_player_not_updated_with_new_campaign(self, mock_get):
        # With
        self.mock_dynamodb.get_item_by_id.return_value = self.player_mock
        self.mock_dynamodb.save_item.return_value = True
        mock_response = MagicMock()
        invalid_campaign_mock = copy.deepcopy(self.campaign_mock)
        invalid_campaign_mock["active_campaigns"][0]["matchers"]["level"] = {
            "min": 98,
            "max": 99
        }
        invalid_campaign_mock["active_campaigns"][0]["name"] = "invalid_campaign"
        mock_response.json = invalid_campaign_mock
        mock_get.return_value = (mock_response, 200)

        # When
        response = self.app.get(f'/get_client_config/{self.player_id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertNotIn("invalid_campaign", response_json["active_campaigns"])
        self.mock_dynamodb.save_item.assert_not_called()

    @patch('controllers.player.CampaignAPI.get')
    def test_player_already_has_current_campaign(self, mock_get):
        # With
        self.mock_dynamodb.get_item_by_id.return_value = self.player_mock
        self.mock_dynamodb.save_item.return_value = True
        mock_response = MagicMock()
        invalid_campaign_mock = copy.deepcopy(self.campaign_mock)
        invalid_campaign_mock["active_campaigns"][0]["name"] = "campaign_1"
        mock_response.json = invalid_campaign_mock
        mock_get.return_value = (mock_response, 200)

        # When
        response = self.app.get(f'/get_client_config/{self.player_id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertEqual(response_json["active_campaigns"].count("campaign_1"), 1)
        self.mock_dynamodb.save_item.assert_not_called()

if __name__ == "__main__":
    unittest.main()
