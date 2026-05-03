from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
    # app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    from .logger import setup_logger
    setup_logger()

    db.init_app(app)
    limiter.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/api")
    from .errors import register_error_handlers
    register_error_handlers(app)

    return app
