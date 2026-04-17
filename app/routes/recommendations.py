"""
Recommendations routes - Advanced SQL-based recommendation algorithm
"""
from flask import Blueprint, render_template, jsonify, request
from app.database import query_db, execute_db

# Create blueprint
recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('/recommendations')
def recommendations():
    """Recommendations page - displays personalized anime recommendations"""
    try:
        # For now using hardcoded user_id = 1 (will use session in Week 3)
        user_id = 1
        
        # Get user's preference summary (top genres, themes, etc.)
        preference_summary = query_db("""
            SELECT * FROM get_user_preference_summary(%s)
        """, (user_id,))
        
        # Organize preferences by type
        top_genres = [p for p in preference_summary if p['preference_type'] == 'Genre']
        top_themes = [p for p in preference_summary if p['preference_type'] == 'Theme']
        top_demographics = [p for p in preference_summary if p['preference_type'] == 'Demographic']
        top_studios = [p for p in preference_summary if p['preference_type'] == 'Studio']
        
        # Get recommendations (top 12 for display)
        recommendations = query_db("""
            SELECT * FROM generate_recommendations(%s, 12)
        """, (user_id,))
        
        # Check if user has rated any anime
        user_ratings_count = query_db("""
            SELECT COUNT(*) as count 
            FROM user_anime_list 
            WHERE user_id = %s AND user_score IS NOT NULL
        """, (user_id,), one=True)
        
        has_ratings = user_ratings_count['count'] > 0
        
        return render_template('recommendations.html',
                             recommendations=recommendations,
                             top_genres=top_genres,
                             top_themes=top_themes,
                             top_demographics=top_demographics,
                             top_studios=top_studios,
                             has_ratings=has_ratings,
                             ratings_count=user_ratings_count['count'])
    
    except Exception as e:
        print(f"Error loading recommendations: {e}")
        return render_template('recommendations.html',
                             recommendations=[],
                             top_genres=[],
                             top_themes=[],
                             top_demographics=[],
                             top_studios=[],
                             has_ratings=False,
                             ratings_count=0,
                             error=str(e))


@recommendations_bp.route('/api/recommendations/refresh', methods=['POST'])
def refresh_recommendations():
    """
    API endpoint to manually refresh user preferences and recommendations
    Useful after user rates new anime
    """
    try:
        user_id = 1  # Hardcoded for now
        
        # Force update of user preferences
        execute_db("""
            SELECT update_all_user_preferences(%s)
        """, (user_id,))
        
        return jsonify({
            'success': True,
            'message': 'Recommendations refreshed successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/api/recommendations/get', methods=['GET'])
def get_recommendations_api():
    """
    API endpoint to get recommendations as JSON
    Optional query params: limit (default 10)
    """
    try:
        user_id = 1  # Hardcoded for now
        limit = request.args.get('limit', 10, type=int)
        
        # Limit max to 50 to prevent abuse
        if limit > 50:
            limit = 50
        
        recommendations = query_db("""
            SELECT * FROM generate_recommendations(%s, %s)
        """, (user_id, limit))
        
        # Convert to list of dicts for JSON
        result = [dict(r) for r in recommendations]
        
        return jsonify({
            'success': True,
            'count': len(result),
            'recommendations': result
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/api/recommendations/preferences', methods=['GET'])
def get_user_preferences():
    """
    API endpoint to get user's preference breakdown
    Shows what genres/themes/etc user likes most
    """
    try:
        user_id = 1  # Hardcoded for now
        
        preferences = query_db("""
            SELECT * FROM get_user_preference_summary(%s)
        """, (user_id,))
        
        # Organize by type
        result = {
            'genres': [dict(p) for p in preferences if p['preference_type'] == 'Genre'],
            'themes': [dict(p) for p in preferences if p['preference_type'] == 'Theme'],
            'demographics': [dict(p) for p in preferences if p['preference_type'] == 'Demographic'],
            'studios': [dict(p) for p in preferences if p['preference_type'] == 'Studio']
        }
        
        return jsonify({
            'success': True,
            'preferences': result
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/api/recommendations/explain/<int:anime_id>', methods=['GET'])
def explain_recommendation(anime_id):
    """
    API endpoint to explain WHY a specific anime was recommended
    Shows the preference scores breakdown
    """
    try:
        user_id = 1  # Hardcoded for now
        
        # Get the recommendation with score breakdown
        explanation = query_db("""
            WITH recommendation AS (
                SELECT * FROM generate_recommendations(%s, 100)
            )
            SELECT * FROM recommendation WHERE anime_id = %s
        """, (user_id, anime_id), one=True)
        
        if not explanation:
            return jsonify({'error': 'Anime not found in recommendations'}), 404
        
        # Get specific matching genres/themes/demographics/studios
        matching_genres = query_db("""
            SELECT g.name, ugp.weighted_score
            FROM anime_genres ag
            JOIN genres g ON ag.genre_id = g.genre_id
            JOIN user_genre_preferences ugp ON g.genre_id = ugp.genre_id
            WHERE ag.anime_id = %s AND ugp.user_id = %s
            ORDER BY ugp.weighted_score DESC
        """, (anime_id, user_id))
        
        matching_themes = query_db("""
            SELECT t.name, utp.weighted_score
            FROM anime_themes at
            JOIN themes t ON at.theme_id = t.theme_id
            JOIN user_theme_preferences utp ON t.theme_id = utp.theme_id
            WHERE at.anime_id = %s AND utp.user_id = %s
            ORDER BY utp.weighted_score DESC
        """, (anime_id, user_id))
        
        return jsonify({
            'success': True,
            'anime': dict(explanation),
            'matching_genres': [dict(g) for g in matching_genres],
            'matching_themes': [dict(t) for t in matching_themes],
            'explanation': f"This anime scored {float(explanation['recommendation_score']):.2f} based on your preferences"
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500