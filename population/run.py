"""
Application entry point
Run this file to start the Flask development server
"""
from app import create_app
import os
 
# Get environment (default to development)
config_name = os.environ.get('FLASK_ENV', 'development')
 
# Create application
app = create_app(config_name)
 
if __name__ == '__main__':
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
 