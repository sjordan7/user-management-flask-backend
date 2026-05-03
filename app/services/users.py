from .. import db
from ..models.users import User
from flask import jsonify
import bcrypt


def create_user(user_data):
    if User.query.filter_by(email=user_data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_pw = bcrypt.hashpw(user_data["password"].encode("utf-8"), bcrypt.gensalt())

    user = User(username=user_data["username"], email=user_data["email"],
                password=hashed_pw.decode("utf-8"), role="user")
    # user = User(**user_data)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201
