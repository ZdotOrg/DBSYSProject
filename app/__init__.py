""" 
Flask application factory for Anime Tracker
"""

from flask import Flask
import os

# Import SQLAlchemy instance
from app.models import db as sqla_db

def create_app(config_class='development'):
    """Application factory function to create and configure the Flask app"""

    app = Flask(__name__,
                template_folder='templates',  # relative to app templates folder
                static_folder='static'  # relative to app static folder
    )

    # Load configuration
    from config import config 
    app.config.from_object(config[config_class])

    # Initialize raw PostgreSQL database (psycopg2)
    from app.database import init_db
    init_db(app)

    # Initialize SQLAlchemy
    sqla_db.init_app(app)
    
    # Create tables if they don't exist (development only)
    if app.config.get('DEBUG'):
        with app.app_context():
            sqla_db.create_all()
            app.logger.info("SQLAlchemy tables created/verified")

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.watchlist import watchlist_bp
    from app.routes.recommendations import recommendations_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(watchlist_bp, url_prefix='/watchlist')
    app.register_blueprint(recommendations_bp, url_prefix='/recommendations')

    # Log startup
    app.logger.info(f"Anime Tracker started with {config_class} config")

    return app