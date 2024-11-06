import logging
import unittest

from flask import Flask

from services.utils import format_response


class TestFormatResponse(unittest.TestCase):
    def setUp(self):
        # Create a Flask app context for testing
        logging.basicConfig(level=logging.CRITICAL)
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Clean up the app context after each test
        self.app_context.pop()

    def test_format_response_success(self):
        # When
        response_data = {"message": "Success"}
        status_code = 200
        response = format_response(status_code, response_data)

        # Assert
        self.assertEqual(response[1], status_code)
        self.assertEqual(response[0].json, response_data)
        self.assertIn("message", response[0].json)
        self.assertEqual(response[0].json["message"], "Success")

    def test_format_response_error(self):
        # When
        response_data = "Bad request"
        status_code = 400
        response_details = "Missing param level"
        response = format_response(status_code, response_data, response_details)

        # Assert
        self.assertEqual(response[1], status_code)
        self.assertEqual(response[0].json["message"], response_data)
        self.assertEqual(response[0].json["details"], response_details)

if __name__ == "__main__":
    unittest.main()
