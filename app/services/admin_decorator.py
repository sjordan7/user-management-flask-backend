from flask import jsonify
from flask_jwt_extended import get_jwt


def admin_required(func):

    def wrapper(*args, **kwargs):
        claims = get_jwt()

        if claims.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return func(*args, **kwargs)
    return wrapper
