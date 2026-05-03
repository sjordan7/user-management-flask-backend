from flask import jsonify
from .exceptions import APIException
import logging


def register_error_handlers(app):
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        logging.error(f"error: {error.message}")
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(Exception)
    def handle_general_exception(error):
        logging.error(f"error: {error.message}")
        return jsonify({"error": "something went wrong"}), 500
