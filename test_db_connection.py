"""
Quick test to verify PostgreSQL connection
Run: python test_db_connection.py
"""
import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Mock Flask app-like object for testing
class MockApp:
    def __init__(self):
        self.config = {
            'DB_HOST': os.environ.get('DB_HOST', 'localhost'),
            'DB_PORT': os.environ.get('DB_PORT', '5432'),
            'DB_NAME': os.environ.get('DB_NAME', 'anime_tracker'),
            'DB_USER': os.environ.get('DB_USER', 'postgres'),
            'DB_PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        }
        self.logger = MockLogger()
    
    def teardown_appcontext(self, func):
        pass

class MockLogger:
    def info(self, msg):
        print(f"ℹ {msg}")
    def error(self, msg):
        print(f" {msg}")

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
    print(" Loaded .env file")
except ImportError:
    print(" python-dotenv not installed, using default values")

# Create mock app and initialize database
app = MockApp()
from database import db

try:
    # Initialize the connection pool
    db.init_app(app)
    
    # Test connection using the query method
    result = db.query_one("SELECT COUNT(*) as count FROM anime")
    count = result['count'] if result else 0
    print(f"Database connected successfully!")
    print(f" Found {count} anime in database")
    
    if count > 0:
        # Get top 5 anime by score
        top_anime = db.query("""
            SELECT title, score, episodes, type
            FROM anime 
            WHERE score IS NOT NULL 
            ORDER BY score DESC 
            LIMIT 5
        """)
        
        print("\n🏆 Top 5 Anime by Score:")
        for i, anime in enumerate(top_anime, 1):
            print(f"  {i}. {anime['title']} - Score: {anime['score']} - {anime['type']}")
        
        # Test a join query
        print("\n📋 Testing genre relationships:")
        anime_with_genres = db.query("""
            SELECT a.title, string_agg(g.name, ', ') as genres
            FROM anime a
            JOIN anime_genres ag ON a.anime_id = ag.anime_id
            JOIN genres g ON ag.genre_id = g.genre_id
            GROUP BY a.anime_id, a.title
            LIMIT 3
        """)
        
        for anime in anime_with_genres:
            print(f"  • {anime['title']}: {anime['genres']}")
    
    # Close all connections
    db.close_all_connections()
    print("\n Database test completed successfully!")
    
except Exception as e:
    print(f" Database connection failed: {e}")
    import traceback
    traceback.print_exc()