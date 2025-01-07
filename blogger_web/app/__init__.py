from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
import json
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
migrate = Migrate()
cache = Cache()


def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config["SECRET_KEY"] = "your_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://flaskuser:flaskpassword@db:5432/flaskdb"
    app.config["CACHE_TYPE"] = "SimpleCache"


    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

    
    # Health check route
    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "ok"}, 200
    
    # Register blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    return app

