import unittest
from uuid import uuid4

from marshmallow import ValidationError

from schemas.player import PlayerSchema


class TestPlayerSchema(unittest.TestCase):

    def setUp(self):
        # Set up a sample valid player data dictionary
        self.valid_data = {
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
            "devices": [],  # Assuming DeviceSchema handles empty list
            "level": 10,
            "xp": 1500,
            "total_playtime": 1000,
            "country": "US",
            "language": "EN",
            "birthdate": "1990-01-01 00:00:00Z",
            "gender": "male",
            "inventory": {"item1": 5, "item2": 3},
            "clan": {
                "id": "123456",
                "name": "Hello world clan"
            }
        }
        self.schema = PlayerSchema()

    def test_valid_data(self):
        """Test loading valid data."""
        result = self.schema.load(self.valid_data)
        self.assertEqual(result["player_id"], self.valid_data["player_id"])
        self.assertEqual(result["level"], self.valid_data["level"])
        self.assertEqual(result["clan"], {
            "id": "123456",
            "name": "Hello world clan"
        })

    def test_missing_required_field(self):
        """Test that missing a required field raises ValidationError."""
        invalid_data = self.valid_data.copy()
        invalid_data.pop("player_id")  # Remove a required field
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)
        self.assertIn("player_id", context.exception.messages)

    def test_invalid_country_length(self):
        """Test that country code with length != 2 raises ValidationError."""
        invalid_data = self.valid_data.copy()
        invalid_data["country"] = "USA"
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)
        self.assertIn("country", context.exception.messages)

    def test_invalid_gender_value(self):
        """Test that an invalid gender value raises ValidationError."""
        invalid_data = self.valid_data.copy()
        invalid_data["gender"] = "unknown"
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)
        self.assertIn("gender", context.exception.messages)

    def test_level_below_minimum(self):
        """Test that level below minimum raises ValidationError."""
        invalid_data = self.valid_data.copy()
        invalid_data["level"] = 0
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)
        self.assertIn("level", context.exception.messages)

    def test_extra_fields_are_included(self):
        """Test that extra fields are included due to unknown=INCLUDE."""
        extra_data = self.valid_data.copy()
        extra_data["extra_field"] = "extra_value"
        result = self.schema.load(extra_data)
        self.assertIn("extra_field", result)
        self.assertEqual(result["extra_field"], "extra_value")

    def test_invalid_date_format(self):
        """Test that an invalid date format raises ValidationError."""
        invalid_data = self.valid_data.copy()
        invalid_data["created"] = "2023-01-01T12:00:00"
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)
        self.assertIn("created", context.exception.messages)

    def test_inventory_key_value_types(self):
        """Test that inventory keys are strings and values are integers."""
        invalid_data = self.valid_data.copy()
        invalid_data["inventory"] = {"item1": "five"}  # invalid value type
        with self.assertRaises(ValidationError) as context:
            self.schema.load(invalid_data)
        self.assertIn("inventory", context.exception.messages)

    def test_optional_fields(self):
        """Test that optional fields can be omitted without errors."""
        optional_data = self.valid_data.copy()
        optional_data.pop("birthdate")  # Remove optional field
        result = self.schema.load(optional_data)
        self.assertNotIn("birthdate", result)

if __name__ == "__main__":
    unittest.main()
