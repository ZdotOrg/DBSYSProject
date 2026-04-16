"""
JIKAN API - FETCH EXTENDED DETAILS
===================================
This module fetches extended anime metadata from Jikan API:
- Characters and voice actors
- Staff members (directors, producers, etc.)
- User reviews
- Recommendations
- Related anime

FEATURES:
    - On-demand fetching (lazy loading)
    - Optional database storage for caching
    - Flask routes for frontend integration

NEW ROUTES:
    GET /api/jikan/<mal_id>/characters    - Get character list
    GET /api/jikan/<mal_id>/staff         - Get staff members
    GET /api/jikan/<mal_id>/reviews       - Get user reviews
    GET /api/jikan/<mal_id>/recommendations - Get similar anime

OPTIONAL DATABASE TABLES:
    If you want to cache this data, run the SQL at the bottom of this file.

INTEGRATION:
    Add to your app/__init__.py:
    
    from jikan_integration.fetch_details import details_bp
    app.register_blueprint(details_bp)
"""

import time
import requests
from flask import Blueprint, request, jsonify, current_app

# Create blueprint
details_bp = Blueprint('jikan_details', __name__, url_prefix='/api/jikan')


# ============================================================
# JIKAN API CONFIGURATION
# ============================================================

JIKAN_BASE_URL = "https://api.jikan.moe/v4"
REQUEST_DELAY = 0.35
RETRY_DELAY = 5
MAX_RETRIES = 3


# ============================================================
# JIKAN API FETCH FUNCTIONS
# ============================================================

def fetch_anime_characters(mal_id):
    """
    Fetch character list for an anime
    
    Args:
        mal_id: MyAnimeList ID
    
    Returns:
        list: Characters with voice actors
    """
    url = f"{JIKAN_BASE_URL}/anime/{mal_id}/characters"
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json().get('data', [])
            elif response.status_code == 429:
                time.sleep(RETRY_DELAY)
            else:
                return []
        
        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    
    return []


def fetch_anime_staff(mal_id):
    """
    Fetch staff list for an anime (directors, writers, etc.)
    
    Args:
        mal_id: MyAnimeList ID
    
    Returns:
        list: Staff members
    """
    url = f"{JIKAN_BASE_URL}/anime/{mal_id}/staff"
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json().get('data', [])
            elif response.status_code == 429:
                time.sleep(RETRY_DELAY)
            else:
                return []
        
        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    
    return []


def fetch_anime_reviews(mal_id, page=1):
    """
    Fetch user reviews for an anime
    
    Args:
        mal_id: MyAnimeList ID
        page: Page number (reviews are paginated)
    
    Returns:
        dict: Reviews data with pagination info
    """
    url = f"{JIKAN_BASE_URL}/anime/{mal_id}/reviews"
    params = {'page': page}
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                time.sleep(RETRY_DELAY)
            else:
                return {'data': [], 'pagination': {}}
        
        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    
    return {'data': [], 'pagination': {}}


def fetch_anime_recommendations(mal_id):
    """
    Fetch recommended anime similar to this one
    
    Args:
        mal_id: MyAnimeList ID
    
    Returns:
        list: Recommended anime
    """
    url = f"{JIKAN_BASE_URL}/anime/{mal_id}/recommendations"
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json().get('data', [])
            elif response.status_code == 429:
                time.sleep(RETRY_DELAY)
            else:
                return []
        
        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    
    return []


def fetch_anime_relations(mal_id):
    """
    Fetch related anime (sequels, prequels, spin-offs, etc.)
    
    Args:
        mal_id: MyAnimeList ID
    
    Returns:
        list: Related anime
    """
    url = f"{JIKAN_BASE_URL}/anime/{mal_id}/relations"
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json().get('data', [])
            elif response.status_code == 429:
                time.sleep(RETRY_DELAY)
            else:
                return []
        
        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    
    return []


# ============================================================
# FLASK ROUTES
# ============================================================

@details_bp.route('/<int:mal_id>/characters', methods=['GET'])
def api_anime_characters(mal_id):
    """
    GET /api/jikan/<mal_id>/characters
    
    Get character list for an anime
    """
    try:
        characters = fetch_anime_characters(mal_id)
        
        # Format response
        formatted = []
        for char_data in characters:
            character = char_data.get('character', {})
            voice_actors = char_data.get('voice_actors', [])
            
            # Get primary voice actor (usually Japanese)
            primary_va = None
            if voice_actors:
                for va in voice_actors:
                    if va.get('language') == 'Japanese':
                        primary_va = {
                            'name': va.get('person', {}).get('name'),
                            'image_url': va.get('person', {}).get('images', {}).get('jpg', {}).get('image_url')
                        }
                        break
                
                # If no Japanese VA, use first one
                if not primary_va and voice_actors:
                    primary_va = {
                        'name': voice_actors[0].get('person', {}).get('name'),
                        'image_url': voice_actors[0].get('person', {}).get('images', {}).get('jpg', {}).get('image_url')
                    }
            
            formatted.append({
                'name': character.get('name'),
                'role': char_data.get('role'),
                'image_url': character.get('images', {}).get('jpg', {}).get('image_url'),
                'mal_id': character.get('mal_id'),
                'voice_actor': primary_va
            })
        
        return jsonify({
            'success': True,
            'count': len(formatted),
            'characters': formatted
        })
    
    except Exception as e:
        current_app.logger.error(f"Characters fetch error: {e}")
        return jsonify({'error': str(e)}), 500


@details_bp.route('/<int:mal_id>/staff', methods=['GET'])
def api_anime_staff(mal_id):
    """
    GET /api/jikan/<mal_id>/staff
    
    Get staff members for an anime
    """
    try:
        staff = fetch_anime_staff(mal_id)
        
        # Format response
        formatted = []
        for staff_member in staff:
            person = staff_member.get('person', {})
            
            formatted.append({
                'name': person.get('name'),
                'positions': staff_member.get('positions', []),
                'image_url': person.get('images', {}).get('jpg', {}).get('image_url'),
                'mal_id': person.get('mal_id')
            })
        
        return jsonify({
            'success': True,
            'count': len(formatted),
            'staff': formatted
        })
    
    except Exception as e:
        current_app.logger.error(f"Staff fetch error: {e}")
        return jsonify({'error': str(e)}), 500


@details_bp.route('/<int:mal_id>/reviews', methods=['GET'])
def api_anime_reviews(mal_id):
    """
    GET /api/jikan/<mal_id>/reviews?page=1
    
    Get user reviews for an anime
    """
    try:
        page = request.args.get('page', 1, type=int)
        
        reviews_data = fetch_anime_reviews(mal_id, page)
        reviews = reviews_data.get('data', [])
        pagination = reviews_data.get('pagination', {})
        
        # Format response
        formatted = []
        for review in reviews:
            user = review.get('user', {})
            
            formatted.append({
                'mal_id': review.get('mal_id'),
                'user': {
                    'username': user.get('username'),
                    'image_url': user.get('images', {}).get('jpg', {}).get('image_url')
                },
                'score': review.get('score'),
                'review': review.get('review'),
                'date': review.get('date'),
                'reactions': review.get('reactions', {}),
                'tags': review.get('tags', [])
            })
        
        return jsonify({
            'success': True,
            'count': len(formatted),
            'reviews': formatted,
            'pagination': {
                'current_page': pagination.get('current_page', 1),
                'has_next_page': pagination.get('has_next_page', False),
                'last_visible_page': pagination.get('last_visible_page', 1)
            }
        })
    
    except Exception as e:
        current_app.logger.error(f"Reviews fetch error: {e}")
        return jsonify({'error': str(e)}), 500


@details_bp.route('/<int:mal_id>/recommendations', methods=['GET'])
def api_anime_recommendations(mal_id):
    """
    GET /api/jikan/<mal_id>/recommendations
    
    Get recommended anime similar to this one
    """
    try:
        recommendations = fetch_anime_recommendations(mal_id)
        
        # Format response
        formatted = []
        for rec in recommendations:
            entry = rec.get('entry', {})
            
            formatted.append({
                'mal_id': entry.get('mal_id'),
                'title': entry.get('title'),
                'image_url': entry.get('images', {}).get('jpg', {}).get('image_url'),
                'url': entry.get('url'),
                'votes': rec.get('votes', 0)
            })
        
        # Sort by votes (most recommended first)
        formatted.sort(key=lambda x: x['votes'], reverse=True)
        
        return jsonify({
            'success': True,
            'count': len(formatted),
            'recommendations': formatted
        })
    
    except Exception as e:
        current_app.logger.error(f"Recommendations fetch error: {e}")
        return jsonify({'error': str(e)}), 500


@details_bp.route('/<int:mal_id>/relations', methods=['GET'])
def api_anime_relations(mal_id):
    """
    GET /api/jikan/<mal_id>/relations
    
    Get related anime (sequels, prequels, etc.)
    """
    try:
        relations = fetch_anime_relations(mal_id)
        
        # Format response
        formatted = []
        for relation in relations:
            relation_type = relation.get('relation')
            entries = relation.get('entry', [])
            
            for entry in entries:
                formatted.append({
                    'relation': relation_type,
                    'mal_id': entry.get('mal_id'),
                    'type': entry.get('type'),
                    'title': entry.get('name'),
                    'url': entry.get('url')
                })
        
        return jsonify({
            'success': True,
            'count': len(formatted),
            'relations': formatted
        })
    
    except Exception as e:
        current_app.logger.error(f"Relations fetch error: {e}")
        return jsonify({'error': str(e)}), 500


@details_bp.route('/<int:mal_id>/full-details', methods=['GET'])
def api_anime_full_details(mal_id):
    """
    GET /api/jikan/<mal_id>/full-details
    
    Get ALL extended details in one request (characters, staff, recommendations, relations)
    Note: This makes multiple API calls, so use sparingly
    """
    try:
        result = {
            'mal_id': mal_id,
            'characters': [],
            'staff': [],
            'recommendations': [],
            'relations': []
        }
        
        # Fetch all data (with delays for rate limiting)
        characters = fetch_anime_characters(mal_id)
        time.sleep(REQUEST_DELAY)
        
        staff = fetch_anime_staff(mal_id)
        time.sleep(REQUEST_DELAY)
        
        recommendations = fetch_anime_recommendations(mal_id)
        time.sleep(REQUEST_DELAY)
        
        relations = fetch_anime_relations(mal_id)
        
        # Format characters (top 10 only)
        for char_data in characters[:10]:
            character = char_data.get('character', {})
            result['characters'].append({
                'name': character.get('name'),
                'role': char_data.get('role'),
                'image_url': character.get('images', {}).get('jpg', {}).get('image_url')
            })
        
        # Format staff (key positions only)
        key_positions = {'Director', 'Original Creator', 'Music', 'Script', 'Character Design'}
        for staff_member in staff:
            person = staff_member.get('person', {})
            positions = staff_member.get('positions', [])
            
            # Check if has key position
            if any(pos in key_positions for pos in positions):
                result['staff'].append({
                    'name': person.get('name'),
                    'positions': positions
                })
        
        # Format recommendations (top 10)
        for rec in recommendations[:10]:
            entry = rec.get('entry', {})
            result['recommendations'].append({
                'mal_id': entry.get('mal_id'),
                'title': entry.get('title'),
                'image_url': entry.get('images', {}).get('jpg', {}).get('image_url')
            })
        
        # Format relations
        for relation in relations:
            relation_type = relation.get('relation')
            entries = relation.get('entry', [])
            
            for entry in entries:
                if entry.get('type') == 'anime':  # Only anime, not manga
                    result['relations'].append({
                        'relation': relation_type,
                        'mal_id': entry.get('mal_id'),
                        'title': entry.get('name')
                    })
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        current_app.logger.error(f"Full details fetch error: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================
# OPTIONAL: DATABASE CACHING TABLES
# ============================================================

"""
If you want to cache extended details in your database, run this SQL:

-- Characters table
CREATE TABLE IF NOT EXISTS anime_characters (
    character_id SERIAL PRIMARY KEY,
    anime_id INTEGER NOT NULL REFERENCES anime(anime_id) ON DELETE CASCADE,
    mal_character_id INTEGER,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50),
    image_url TEXT,
    voice_actor_name VARCHAR(255),
    voice_actor_image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_anime_characters_anime ON anime_characters(anime_id);

-- Staff table
CREATE TABLE IF NOT EXISTS anime_staff (
    staff_id SERIAL PRIMARY KEY,
    anime_id INTEGER NOT NULL REFERENCES anime(anime_id) ON DELETE CASCADE,
    mal_person_id INTEGER,
    name VARCHAR(255) NOT NULL,
    positions TEXT[], -- Array of positions
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_anime_staff_anime ON anime_staff(anime_id);

-- Reviews cache (optional)
CREATE TABLE IF NOT EXISTS anime_reviews_cache (
    review_id SERIAL PRIMARY KEY,
    anime_id INTEGER NOT NULL REFERENCES anime(anime_id) ON DELETE CASCADE,
    mal_review_id INTEGER,
    username VARCHAR(100),
    user_image TEXT,
    score INTEGER,
    review_text TEXT,
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_anime_reviews_anime ON anime_reviews_cache(anime_id);
"""