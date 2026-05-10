from .. import db
from ..models.users import User
from ..exceptions import NotFoundError, UnauthorizedError, ForbiddenError
from ..repositories.user_repo import get_user_by_email, create_user, get_user_by_id
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import jsonify
import bcrypt


def signup_user(user_data):
    # if User.query.filter_by(email=user_data["email"]).first():
    if get_user_by_email(user_data["email"]):
        return jsonify({"message": "Email already exists"}), 400

    hashed_pw = bcrypt.hashpw(user_data["password"].encode("utf-8"), bcrypt.gensalt())

    user = User(username=user_data["username"], email=user_data["email"],
                password=hashed_pw.decode("utf-8"), role="user")
    # user = User(**user_data)
    user = create_user(user)
    # print(user.email)

    return jsonify(user.to_dict()), 201


def login_user(user_data):
    user = get_user_by_email(user_data["email"])
    if not user:
        # return jsonify({"error": "Invalid credentials"}), 401
        # logging.error("User not found")
        raise NotFoundError("User not found")

    if not bcrypt.checkpw(user_data["password"].encode("utf-8"), user.password.encode("utf-8")):
        # return jsonify({"error": "Invalid credentials"}), 401
        # logging.error("Invalid credentials")
        raise UnauthorizedError("Invalid credentials")
    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return access_token


def delete_user_id(user_id):
    user = get_user_by_id(user_id)

    if not user:
        # return jsonify({"error": "User not found"}), 404
        # logging.error("User not found")
        raise NotFoundError("User not found")

    return delete_user(user)







