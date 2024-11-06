from flask import current_app as app
from flask import jsonify


def format_response(status_code, response="", details=""):
    #TODO: Make sure we don't diplay PII here
    if status_code in range(200, 300):
        app.logger.debug(response)
    else:
        response = {
            "message": response,
            "details": details
        }
        app.logger.error(response)
    return jsonify(response), status_code
