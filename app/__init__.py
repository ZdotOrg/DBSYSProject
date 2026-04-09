""" 
Flask application factory for Anime Tracker
"""

from flask import Flask
import os

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
    
    # Test database connection on startup
    with app.app_context():
        try:
            from app.database import query_db
            result = query_db("SELECT COUNT(*) as count FROM anime", one=True)
            app.logger.info(f" Database connected. Found {result['count']} anime.")
        except Exception as e:
            app.logger.error(f" Database connection failed: {e}")

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