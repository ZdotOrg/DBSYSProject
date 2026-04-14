"""
Flask application factory for Anime Tracker
"""

import os
from flask import Flask
from population.config import config


def create_app(config_class='development'):
    """Application factory function to create and configure the Flask app"""

    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(
        __name__,
        template_folder=os.path.join(basedir, 'templates'),
        static_folder=os.path.join(basedir, 'static')
    )

    # Load configuration
    app.config.from_object(config.get(config_class, config['default']))

    # Initialize raw PostgreSQL database (psycopg2)
    from app.database import init_db
    init_db(app)

    # Test database connection on startup
    with app.app_context():
        try:
            from app.database import query_db
            result = query_db("SELECT COUNT(*) as count FROM anime", one=True)
            app.logger.info(f"Database connected. Found {result['count']} anime.")
        except Exception as e:
            app.logger.error(f"Database connection failed: {e}")

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.watchlist import watchlist_bp
    from app.routes.recommendations import recommendations_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(watchlist_bp)
    app.register_blueprint(recommendations_bp)

    # Log startup
    app.logger.info(f"Anime Tracker started with {config_class} config")

    return app