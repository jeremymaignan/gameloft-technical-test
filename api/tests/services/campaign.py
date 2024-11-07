import copy
import unittest

from services.campaign import (does_not_have_attr, has_attr, is_valid_campaign,
                               is_valid_level)


class TestCampaignFunctions(unittest.TestCase):
    #pylint: disable=too-many-instance-attributes
    campaign = {
        "matchers": {
            "level": {"min": 10, "max": 20},
            "has": {
                "items": ["sword", "shield"],
                "country": ["US", "Canada"],
                "language": ["English"],
                "gender": ["male", "female"]
            },
            "does_not_have": {
                "items": ["axe"],
                "country": ["MX"],
                "language": ["Spanish"],
                "gender": ["other"]
            }
        }
    }

    player_valid = {
        "level": 15,
        "inventory": {"sword": 1, "shield": 1},
        "country": "US",
        "language": "English",
        "gender": "male"
    }

    player_invalid_level = {
        "level": 5,
        "inventory": {"sword": 1, "shield": 1},
        "country": "US",
        "language": "English",
        "gender": "male"
    }

    player_invalid_has = {
        "level": 15,
        "inventory": {"shield": 1},  # Missing "sword"
        "country": "US",
        "language": "English",
        "gender": "male"
    }

    player_invalid_does_not_have = {
        "level": 15,
        "inventory": {"sword": 1, "shield": 1, "axe": 1},  # Has "axe"
        "country": "US",
        "language": "English",
        "gender": "male"
    }

    player_invalid_country = {
        "level": 15,
        "inventory": {"sword": 1, "shield": 1},
        "country": "MX",  # Invalid country
        "language": "English",
        "gender": "male"
    }

    player_invalid_language = {
        "level": 15,
        "inventory": {"sword": 1, "shield": 1},
        "country": "US",
        "language": "Spanish",  # Invalid language
        "gender": "male"
    }

    player_invalid_gender = {
        "level": 15,
        "inventory": {"sword": 1, "shield": 1},
        "country": "US",
        "language": "English",
        "gender": "other"  # Invalid gender
    }

    player_without_country = {
        "level": 15,
        "inventory": {"sword": 1, "shield": 1},
        "language": "English",
        "gender": "male"
    }

    def test_is_valid_level(self):
        self.assertTrue(is_valid_level(self.campaign["matchers"], self.player_valid))
        self.assertFalse(is_valid_level(self.campaign["matchers"], self.player_invalid_level))

        missing_level = copy.deepcopy(self.campaign)
        del missing_level["matchers"]["level"]
        self.assertTrue(is_valid_level(missing_level["matchers"], self.player_valid))

    def test_has_attr(self):
        self.assertTrue(has_attr(self.campaign["matchers"], self.player_valid))
        self.assertFalse(has_attr(self.campaign["matchers"], self.player_invalid_has))
        self.assertFalse(has_attr(self.campaign["matchers"], self.player_invalid_country))
        self.assertFalse(has_attr(self.campaign["matchers"], self.player_invalid_language))
        self.assertFalse(has_attr(self.campaign["matchers"], self.player_invalid_gender))
        self.assertFalse(has_attr(self.campaign["matchers"], self.player_without_country))

        missing_has = copy.deepcopy(self.campaign)
        del missing_has["matchers"]["has"]
        self.assertTrue(has_attr(missing_has["matchers"], self.player_valid))

    def test_does_not_have_attr(self):
        self.assertTrue(does_not_have_attr(self.campaign["matchers"], self.player_valid))
        self.assertFalse(does_not_have_attr(self.campaign["matchers"],
                                             self.player_invalid_does_not_have))
        self.assertFalse(does_not_have_attr(self.campaign["matchers"], self.player_without_country))

        missing_does_not_have = copy.deepcopy(self.campaign)
        del missing_does_not_have["matchers"]["does_not_have"]
        self.assertTrue(does_not_have_attr(missing_does_not_have["matchers"], self.player_valid))

    def test_is_valid_campaign(self):
        self.assertTrue(is_valid_campaign(self.campaign, self.player_valid))
        self.assertFalse(is_valid_campaign(self.campaign, self.player_invalid_level))
        self.assertFalse(is_valid_campaign(self.campaign, self.player_invalid_has))
        self.assertFalse(is_valid_campaign(self.campaign, self.player_invalid_does_not_have))
        self.assertFalse(is_valid_campaign(self.campaign, self.player_invalid_country))
        self.assertFalse(is_valid_campaign(self.campaign, self.player_invalid_language))
        self.assertFalse(is_valid_campaign(self.campaign, self.player_invalid_gender))

        missing_matchers = copy.deepcopy(self.campaign)
        del missing_matchers["matchers"]
        self.assertTrue(does_not_have_attr(missing_matchers, self.player_valid))

if __name__ == "__main__":
    unittest.main()
