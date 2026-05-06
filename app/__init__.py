from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from celery import Celery
from .celery_app import celery, init_celery
from .tasks import email_tasks


limiter = Limiter(key_func=get_remote_address)
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
load_dotenv()
cache = Cache()
celery = None


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
    # app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
    app.config["CACHE_TYPE"] = os.getenv("CACHE_TYPE", "SimpleCache")
    app.config["CACHE_REDIS_URL"] = os.getenv("CACHE_REDIS_URL")
    app.config["CACHE_DEFAULT_TIMEOUT"] = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 60))
    app.config["CELERY_BROKER_URL"] = os.getenv("CELERY_BROKER_URL")
    app.config["CELERY_RESULT_BACKEND"] = os.getenv("CELERY_RESULT_BACKEND")

    from .logger import setup_logger
    setup_logger()

    db.init_app(app)
    limiter.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    init_celery(app)

    # import tasks

    # import tasks

    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/api")
    from .errors import register_error_handlers
    register_error_handlers(app)

    return app
