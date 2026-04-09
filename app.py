"""
Anime Tracker - Main Flask Application
"""
import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

# Create application from package factory
app = create_app(os.environ.get('FLASK_CONFIG', 'default'))

# ============================================================================
# Main entrypoint
# ============================================================================

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', True), host='0.0.0.0', port=5000)
