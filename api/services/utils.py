from flask import \
    current_app as app  # Import current_app to access the app context
from flask import jsonify


def format_response(response, status_code):
    #TODO: make sure we don't diplay PII here
    if status_code in range(200, 300):
        app.logger.debug(response)
        return jsonify(response), status_code
    # Error reponses
    app.logger.error(response)
    return jsonify({"error": response}), status_code
