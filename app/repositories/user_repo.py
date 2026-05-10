from ..models.users import User
from .. import db


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def create_user(user):
    db.session.add(user)
    db.session.commit()
    return user


def get_all_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    return user

