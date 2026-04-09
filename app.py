"""
Anime Tracker - Main Flask Application
"""
from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
from database import db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# ============================================================================
# ROUTES - Main Pages
# ============================================================================

@app.route('/')
def index():
    """Home page with featured anime"""
    return render_template('index.html')

@app.route('/search')
def search_page():
    """Search page"""
    return render_template('search.html')

@app.route('/watchlist')
def watchlist_page():
    """User's watchlist page"""
    return render_template('watchlist.html')

@app.route('/recommendations')
def recommendations_page():
    """Personalized recommendations page"""
    return render_template('recommendations.html')

# ============================================================================
# API ENDPOINTS - Anime Data
# ============================================================================

@app.route('/api/anime')
def get_anime():
    """Get anime list with optional filters"""
    try:
        # Get query parameters
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        search = request.args.get('search', '')
        min_score = request.args.get('min_score', type=float)
        
        # Build query
        query = """
            SELECT anime_id, title, title_english, synopsis, episodes, 
                   score, rank, popularity, image_url, status
            FROM anime
            WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND (title ILIKE %s OR title_english ILIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param])
        
        if min_score:
            query += " AND score >= %s"
            params.append(min_score)
        
        query += " ORDER BY popularity LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        results = db.execute_query(query, tuple(params))
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/anime/<int:anime_id>')
def get_anime_detail(anime_id):
    """Get detailed information for a specific anime"""
    try:
        query = """
            SELECT * FROM anime WHERE anime_id = %s
        """
        result = db.execute_query(query, (anime_id,))
        
        if result:
            return jsonify(result[0])
        else:
            return jsonify({'error': 'Anime not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# API ENDPOINTS - User Watchlist & Ratings
# ============================================================================

@app.route('/api/watchlist', methods=['GET'])
def get_watchlist():
    """Get user's watchlist"""
    # For now, using demo user (user_id = 1)
    # In production, you'd get this from session
    user_id = 1
    
    try:
        query = """
            SELECT w.watchlist_id, w.priority, w.notes, w.added_at,
                   a.anime_id, a.title, a.image_url, a.episodes, a.score,
                   ur.watch_status, ur.episodes_watched, ur.rating
            FROM watchlist w
            JOIN anime a ON w.anime_id = a.anime_id
            LEFT JOIN user_ratings ur ON w.user_id = ur.user_id 
                AND w.anime_id = ur.anime_id
            WHERE w.user_id = %s
            ORDER BY w.priority DESC, w.added_at DESC
        """
        results = db.execute_query(query, (user_id,))
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/watchlist', methods=['POST'])
def add_to_watchlist():
    """Add anime to watchlist"""
    user_id = 1  # Demo user
    data = request.json
    
    try:
        query = """
            INSERT INTO watchlist (user_id, anime_id, priority, notes)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, anime_id) DO NOTHING
            RETURNING watchlist_id
        """
        result = db.execute_query(
            query, 
            (user_id, data['anime_id'], data.get('priority', 0), data.get('notes', '')),
            fetch=True
        )
        
        if result:
            return jsonify({'success': True, 'watchlist_id': result[0]['watchlist_id']})
        else:
            return jsonify({'success': False, 'message': 'Already in watchlist'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/watchlist/<int:watchlist_id>', methods=['DELETE'])
def remove_from_watchlist(watchlist_id):
    """Remove anime from watchlist"""
    try:
        query = "DELETE FROM watchlist WHERE watchlist_id = %s"
        db.execute_query(query, (watchlist_id,), fetch=False)
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rating', methods=['POST'])
def update_rating():
    """Update user rating for an anime"""
    user_id = 1  # Demo user
    data = request.json
    
    try:
        query = """
            INSERT INTO user_ratings (user_id, anime_id, rating, watch_status, episodes_watched)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id, anime_id) 
            DO UPDATE SET 
                rating = EXCLUDED.rating,
                watch_status = EXCLUDED.watch_status,
                episodes_watched = EXCLUDED.episodes_watched,
                last_updated = CURRENT_TIMESTAMP
            RETURNING rating_id
        """
        result = db.execute_query(
            query,
            (user_id, data['anime_id'], data.get('rating'), 
             data.get('watch_status'), data.get('episodes_watched', 0)),
            fetch=True
        )
        
        return jsonify({'success': True, 'rating_id': result[0]['rating_id']})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# API ENDPOINTS - Recommendations
# ============================================================================

@app.route('/api/recommendations')
def get_recommendations():
    """Get personalized anime recommendations"""
    user_id = 1  # Demo user
    
    try:
        # Simple recommendation algorithm based on:
        # 1. User's highest rated anime
        # 2. Popular anime they haven't watched
        # 3. Time decay factor for recent interactions
        
        query = """
            WITH user_preferences AS (
                SELECT 
                    anime_id,
                    rating,
                    calculate_time_decay(last_updated) as recency_weight
                FROM user_ratings
                WHERE user_id = %s AND rating >= 7.0
            ),
            watched_anime AS (
                SELECT anime_id FROM user_ratings WHERE user_id = %s
            )
            SELECT 
                a.anime_id,
                a.title,
                a.image_url,
                a.score,
                a.episodes,
                a.synopsis,
                (a.score / 10.0 * a.popularity::numeric / 1000.0) as recommendation_score
            FROM anime a
            WHERE a.anime_id NOT IN (SELECT anime_id FROM watched_anime)
                AND a.score >= 7.0
                AND a.members >= 10000
            ORDER BY recommendation_score DESC
            LIMIT 20
        """
        
        results = db.execute_query(query, (user_id, user_id))
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# API ENDPOINTS - User Stats
# ============================================================================

@app.route('/api/stats')
def get_user_stats():
    """Get user statistics"""
    user_id = 1  # Demo user
    
    try:
        query = "SELECT * FROM user_stats WHERE user_id = %s"
        result = db.execute_query(query, (user_id,))
        
        if result:
            return jsonify(result[0])
        else:
            return jsonify({
                'total_anime': 0,
                'completed_count': 0,
                'watching_count': 0,
                'avg_rating': 0,
                'total_episodes_watched': 0
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)