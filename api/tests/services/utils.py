import logging
import unittest

from flask import Flask

from services.utils import format_response


class TestFormatResponse(unittest.TestCase):
    def setUp(self):
        # Create a Flask app context for testing
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()  # Push the app context to the current_ap
        logging.basicConfig(level=logging.CRITICAL)

    def tearDown(self):
        self.app_context.pop()  # Clean up the app context after each test

    def test_format_response_success(self):
        response_data = {"message": "Success"}
        status_code = 200

        with self.app.test_request_context():  # Use a request context
            response = format_response(status_code, response_data)
            self.assertEqual(response[1], status_code)  # Check status code
            self.assertEqual(response[0].json, response_data)  # Check JSON response
            self.assertIn("message", response[0].json)  # Check if 'message' is in the response
            self.assertEqual(response[0].json["message"], "Success")  # Validate message content

    def test_format_response_client_error(self):
        response_data = "Bad request"
        status_code = 400

        with self.app.test_request_context():  # Use a request context
            response = format_response(status_code, response_data)
            self.assertEqual(response[1], status_code)  # Check status code
            self.assertIn("message", response[0].json)  # Check for 'error' key
            self.assertEqual(response[0].json["message"], response_data)  # Validate error message

    def test_format_response_server_error(self):
        response_data = "Internal Server Error"
        status_code = 500

        with self.app.test_request_context():  # Use a request context
            response = format_response(status_code, response_data)
            self.assertEqual(response[1], status_code)  # Check status code
            self.assertIn("message", response[0].json)  # Check for 'error' key
            self.assertEqual(response[0].json["message"], response_data)  # Validate error message

if __name__ == "__main__":
    unittest.main()
