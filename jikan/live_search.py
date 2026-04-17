"""
JIKAN API - LIVE SEARCH ROUTES
===============================
This module adds Flask routes for searching anime directly from Jikan API.
Allows users to discover anime not yet in your database and import them.

FEATURES:
    - Search Jikan API in real-time
    - Display results alongside database results
    - Import selected anime to database
    - Caching to reduce API calls

NEW ROUTES:
    GET  /api/jikan/search?q=naruto          - Search Jikan API
    POST /api/jikan/import                   - Import anime to database
    GET  /api/jikan/anime/<mal_id>           - Get anime details from Jikan

INTEGRATION:
    Add this to your app/__init__.py:
    
    from jikan_integration.live_search import jikan_bp
    app.register_blueprint(jikan_bp)
"""

import time
import requests
from flask import Blueprint, request, jsonify, current_app
from functools import lru_cache

# Import database functions from populate script
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from populate_database import (
    insert_anime, anime_exists,
    JIKAN_BASE_URL, REQUEST_DELAY, MAX_RETRIES, RETRY_DELAY
)

# Create blueprint
jikan_bp = Blueprint('jikan', __name__)


# ============================================================
# JIKAN API SEARCH FUNCTIONS
# ============================================================

def search_jikan_anime(query, limit=10):
    """
    Search anime on Jikan API by title
    
    Args:
        query: Search query string
        limit: Max results to return
    
    Returns:
        list: Anime results
    """
    if not query or len(query) < 2:
        return []
    
    url = f"{JIKAN_BASE_URL}/anime"
    params = {
        'q': query,
        'limit': limit,
        'order_by': 'popularity',
        'sort': 'asc'
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            elif response.status_code == 429:
                time.sleep(RETRY_DELAY)
            else:
                break
        
        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    
    return []


def get_jikan_anime_by_id(mal_id):
    """
    Get anime details from Jikan API by MAL ID
    
    Args:
        mal_id: MyAnimeList ID
    
    Returns:
        dict: Anime data
    """
    url = f"{JIKAN_BASE_URL}/anime/{mal_id}/full"
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json().get('data')
            elif response.status_code == 429:
                time.sleep(RETRY_DELAY)
            else:
                return None
        
        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    
    return None


# ============================================================
# FLASK ROUTES
# ============================================================

@jikan_bp.route('/search', methods=['GET'])
def api_jikan_search():
    """
    GET /api/jikan/search?q=naruto&limit=10
    
    Search anime on Jikan API and return results
    Marks anime already in database with 'in_database' flag
    """
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 10, type=int)
        
        if not query:
            return jsonify({'error': 'Query parameter required'}), 400
        
        if limit > 25:
            limit = 25  # Jikan API max
        
        # Search Jikan
        results = search_jikan_anime(query, limit)
        
        if not results:
            return jsonify({
                'success': True,
                'count': 0,
                'results': []
            })
        
        # Check which anime are already in our database
        from app.database import db
        conn = db.get_connection()
        
        try:
            for anime in results:
                mal_id = anime.get('mal_id')
                anime['in_database'] = anime_exists(conn, mal_id)
        finally:
            db.return_connection(conn)
        
        # Format results
        formatted_results = []
        for anime in results:
            images = anime.get('images', {}).get('jpg', {})
            formatted_results.append({
                'mal_id': anime.get('mal_id'),
                'title': anime.get('title'),
                'title_english': anime.get('title_english'),
                'type': anime.get('type'),
                'episodes': anime.get('episodes'),
                'score': anime.get('score'),
                'image_url': images.get('image_url'),
                'synopsis': anime.get('synopsis'),
                'in_database': anime.get('in_database', False)
            })
        
        return jsonify({
            'success': True,
            'count': len(formatted_results),
            'results': formatted_results
        })
    
    except Exception as e:
        current_app.logger.error(f"Jikan search error: {e}")
        return jsonify({'error': str(e)}), 500


@jikan_bp.route('/anime/<int:mal_id>', methods=['GET'])
def api_jikan_anime_details(mal_id):
    """
    GET /api/jikan/anime/<mal_id>
    
    Get full anime details from Jikan API
    """
    try:
        anime_data = get_jikan_anime_by_id(mal_id)
        
        if not anime_data:
            return jsonify({'error': 'Anime not found on MyAnimeList'}), 404
        
        # Check if in database
        from app.database import db
        conn = db.get_connection()
        
        try:
            in_db = anime_exists(conn, mal_id)
        finally:
            db.return_connection(conn)
        
        anime_data['in_database'] = in_db
        
        return jsonify({
            'success': True,
            'data': anime_data
        })
    
    except Exception as e:
        current_app.logger.error(f"Jikan anime details error: {e}")
        return jsonify({'error': str(e)}), 500


@jikan_bp.route('/import', methods=['POST'])
def api_jikan_import():
    """
    POST /api/jikan/import
    Body: {"mal_id": 12345}
    
    Import an anime from Jikan API into your database
    """
    try:
        data = request.get_json()
        
        if not data or 'mal_id' not in data:
            return jsonify({'error': 'mal_id required'}), 400
        
        mal_id = data['mal_id']
        
        # Check if already exists
        from app.database import db
        conn = db.get_connection()
        
        try:
            if anime_exists(conn, mal_id):
                return jsonify({
                    'success': False,
                    'message': 'Anime already in database'
                }), 400
            
            # Fetch from Jikan
            anime_data = get_jikan_anime_by_id(mal_id)
            
            if not anime_data:
                return jsonify({'error': 'Anime not found on MyAnimeList'}), 404
            
            # Insert into database
            anime_id = insert_anime(conn, anime_data)
            
            if anime_id:
                return jsonify({
                    'success': True,
                    'message': 'Anime imported successfully',
                    'anime_id': anime_id,
                    'mal_id': mal_id,
                    'title': anime_data.get('title')
                }), 201
            else:
                return jsonify({'error': 'Failed to import anime'}), 500
        
        finally:
            db.return_connection(conn)
    
    except Exception as e:
        current_app.logger.error(f"Jikan import error: {e}")
        return jsonify({'error': str(e)}), 500


@jikan_bp.route('/batch-import', methods=['POST'])
def api_jikan_batch_import():
    """
    POST /api/jikan/batch-import
    Body: {"mal_ids": [12345, 67890, ...]}
    
    Import multiple anime from Jikan API
    """
    try:
        data = request.get_json()
        
        if not data or 'mal_ids' not in data:
            return jsonify({'error': 'mal_ids array required'}), 400
        
        mal_ids = data['mal_ids']
        
        if not isinstance(mal_ids, list):
            return jsonify({'error': 'mal_ids must be an array'}), 400
        
        if len(mal_ids) > 10:
            return jsonify({'error': 'Maximum 10 anime per batch'}), 400
        
        from app.database import db
        conn = db.get_connection()
        
        results = {
            'imported': [],
            'skipped': [],
            'failed': []
        }
        
        try:
            for mal_id in mal_ids:
                # Check if exists
                if anime_exists(conn, mal_id):
                    results['skipped'].append({
                        'mal_id': mal_id,
                        'reason': 'Already in database'
                    })
                    continue
                
                # Fetch from Jikan
                anime_data = get_jikan_anime_by_id(mal_id)
                
                if not anime_data:
                    results['failed'].append({
                        'mal_id': mal_id,
                        'reason': 'Not found on MAL'
                    })
                    continue
                
                # Insert
                anime_id = insert_anime(conn, anime_data)
                
                if anime_id:
                    results['imported'].append({
                        'mal_id': mal_id,
                        'anime_id': anime_id,
                        'title': anime_data.get('title')
                    })
                else:
                    results['failed'].append({
                        'mal_id': mal_id,
                        'reason': 'Database insertion failed'
                    })
                
                # Rate limiting
                time.sleep(REQUEST_DELAY)
        
        finally:
            db.return_connection(conn)
        
        return jsonify({
            'success': True,
            'results': results,
            'summary': {
                'imported': len(results['imported']),
                'skipped': len(results['skipped']),
                'failed': len(results['failed'])
            }
        })
    
    except Exception as e:
        current_app.logger.error(f"Jikan batch import error: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================
# HELPER ROUTE: CHECK DATABASE STATUS
# ============================================================

@jikan_bp.route('/check/<int:mal_id>', methods=['GET'])
def api_jikan_check(mal_id):
    """
    GET /api/jikan/check/<mal_id>
    
    Check if an anime (by MAL ID) is in your database
    """
    try:
        from app.database import db
        conn = db.get_connection()
        
        try:
            exists = anime_exists(conn, mal_id)
            
            if exists:
                # Get anime_id from database
                cur = conn.cursor()
                cur.execute("SELECT anime_id, title FROM anime WHERE mal_id = %s", (mal_id,))
                result = cur.fetchone()
                cur.close()
                
                return jsonify({
                    'in_database': True,
                    'anime_id': result[0] if result else None,
                    'title': result[1] if result else None
                })
            else:
                return jsonify({'in_database': False})
        
        finally:
            db.return_connection(conn)
    
    except Exception as e:
        current_app.logger.error(f"Jikan check error: {e}")
        return jsonify({'error': str(e)}), 500