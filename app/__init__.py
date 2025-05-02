import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Suppress warning
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev') # Default to 'dev' if not set

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Alembic can detect them
    from . import models

    from .routes import bp as main_bp
    app.register_blueprint(main_bp) # Register the main blueprint

    return app
