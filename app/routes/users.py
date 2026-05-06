from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from .. import db
from ..models.users import User
from ..schemas.user_schema import UserSchema
from ..services.users import signup_user, login_user, delete_user_id
from ..services.admin_decorator import admin_required
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..exceptions import NotFoundError, UnauthorizedError, ForbiddenError
import logging
from .. import limiter
from .. import cache
from ..tasks.email_tasks import send_email_task


users_bp = Blueprint("users", __name__)
user_schema = UserSchema()


@users_bp.route("/", methods=["GET"])
def home():
    return "Welcome!"


@users_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = signup_user(data)
    # print(user)

    #async task as delay sends task to queue
    send_email_task.delay(data["email"])

    return user


@users_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()

    access_token = login_user(data)
    logging.info("Login Successful")
    return jsonify({"message": "Login Successful",
                    "access_token": access_token}), 200


@users_bp.route("/users", methods=["GET"])
@jwt_required()
@cache.cached()
def list_users():
    keyword = request.args.get("keyword", "")
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    # users = User.query.all()

    current_user_id = get_jwt_identity()

    query = User.query

    if keyword:
        query = query.filter(User.username.ilike(f'%{keyword}%'))

    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    users = pagination.items

    return jsonify({
        "page": page,
        "limit": limit,
        "total": pagination.total,
        "current_user": current_user_id,
        "data": [u.to_dict() for u in users]
    }), 200

    # return jsonify([u.to_dict() for u in users]), 200


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user_by_id(user_id):
    user = delete_user_id(user_id)
    logging.info("User deleted")
    return jsonify({"message": f"{user} deleted"}), 200

