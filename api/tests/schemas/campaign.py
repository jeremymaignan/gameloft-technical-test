import unittest
from datetime import datetime
from uuid import UUID, uuid4

from marshmallow import ValidationError

from schemas.player import PlayerSchema


class TestPlayerSchema(unittest.TestCase):
    valid_player = {
        "player_id": uuid4(),
        "credential": "sample_credential",
        "created": "2023-01-01 12:00:00Z",
        "modified": "2023-01-02 12:00:00Z",
        "last_session": "2023-01-02 13:00:00Z",
        "total_spent": 100,
        "total_refund": 10,
        "total_transactions": 5,
        "last_purchase": "2023-01-02 12:00:00Z",
        "active_campaigns": ["campaign_1", "campaign_2"],
        "devices": [{
            "id": 1,
            "model": "apple iphone 11",
            "carrier": "vodafone",
            "firmware": "123"
        }],
        "level": 10,
        "xp": 1500,
        "total_playtime": 1000,
        "country": "US",
        "language": "en",
        "birthdate": "1990-01-01 00:00:00Z",
        "gender": "male",
        "inventory": {"item1": 5, "item2": 3},
        "clan": {
            "id": "123456",
            "name": "Hello world clan"
        }
    }
    schema = PlayerSchema()

    def test_valid_data(self):
        # When
        result = self.schema.load(self.valid_player)

        # Assert
        self.assertEqual(result["player_id"], self.valid_player["player_id"])
        self.assertEqual(result["level"], self.valid_player["level"])
        self.assertEqual(result["clan"], {
            "id": "123456",
            "name": "Hello world clan"
        })

    def test_missing_required_field(self):
        # With
        invalid_data = self.valid_player.copy()
        invalid_data.pop("player_id")

        # When
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)

        # Assert
        self.assertIn("player_id", context.exception.messages)

    def test_invalid_country_format(self):
        # With
        invalid_data = self.valid_player.copy()
        invalid_data["country"] = "USA"

        # When
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)

        # Assert
        self.assertIn("country", context.exception.messages)

    def test_invalid_gender_value(self):
        # With
        invalid_data = self.valid_player.copy()
        invalid_data["gender"] = "unknown"

        # When
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)

        # Assert
        self.assertIn("gender", context.exception.messages)

    def test_level_below_minimum(self):
        # With
        invalid_data = self.valid_player.copy()
        invalid_data["level"] = 0

        # When
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)

        # Assert
        self.assertIn("level", context.exception.messages)

    def test_extra_fields_are_included(self):
        # With
        extra_data = self.valid_player.copy()
        extra_data["extra_field"] = "extra_value"

        # When
        result = self.schema.load(extra_data)

        # Assert
        self.assertIn("extra_field", result)
        self.assertEqual(result["extra_field"], "extra_value")

    def test_invalid_date_format(self):
        # With
        invalid_data = self.valid_player.copy()
        invalid_data["created"] = "2023-01-01T12:00:00"

        # When
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)

        # Assert
        self.assertIn("created", context.exception.messages)

    def test_inventory_key_value_types(self):
        # With
        invalid_data = self.valid_player.copy()
        invalid_data["inventory"] = {"item1": "five"}  # invalid value type

        # When
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)

        # Assert
        self.assertIn("inventory", context.exception.messages)

    def test_optional_fields(self):
        # With
        optional_data = self.valid_player.copy()
        optional_data.pop("last_purchase")

        # When
        result = self.schema.load(optional_data)

        # Assert
        self.assertNotIn("last_purchase", result)

    def test_dump_valid_data(self):
        # With
        player_obj = self.valid_player.copy()
        player_obj.update({
            "player_id": UUID("33c68541-c7a7-49a1-ac18-43949b81c026"),
            "created": datetime(2025, 1, 1, 12, 0),
            "modified": datetime(2025, 1, 2, 12, 0),
            "last_session": datetime(2025, 1, 2, 13, 0),
            "last_purchase": datetime(2025, 1, 2, 12, 0),
            "birthdate": datetime(1995, 1, 1, 0, 0),
        })

        # When
        result = self.schema.dump(player_obj)

        # Assert
        self.assertEqual(result["player_id"], "33c68541-c7a7-49a1-ac18-43949b81c026")
        self.assertEqual(result["created"], "2025-01-01 12:00:00Z")
        self.assertEqual(result["modified"], "2025-01-02 12:00:00Z")
        self.assertEqual(result["last_session"], "2025-01-02 13:00:00Z")
        self.assertEqual(result["last_purchase"], "2025-01-02 12:00:00Z")
        self.assertEqual(result["birthdate"], "1995-01-01 00:00:00Z")

if __name__ == "__main__":
    unittest.main()
