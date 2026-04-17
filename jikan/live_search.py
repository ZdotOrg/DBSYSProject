"""
JIKAN API - LIVE SEARCH ROUTES (OPTIMIZED)
=======================================
Self-contained Jikan API integration with performance improvements
"""

import time
import requests
from flask import Blueprint, request, jsonify, current_app

# Create blueprint
jikan_bp = Blueprint('jikan', __name__)

# Constants
JIKAN_BASE_URL = "https://api.jikan.moe/v4"
MAX_RETRIES = 2  # Reduced for faster failure
RETRY_DELAY = 1  # Reduced delay
REQUEST_TIMEOUT = 8  # Seconds


def search_jikan_anime(query, limit=10):
    """Search anime on Jikan API with better error handling"""
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
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            elif response.status_code == 429:
                # Rate limited - wait and retry
                time.sleep(RETRY_DELAY * (attempt + 1))
            elif response.status_code == 404:
                return []
            else:
                current_app.logger.warning(f"Jikan API error: {response.status_code}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
        
        except requests.exceptions.Timeout:
            current_app.logger.warning(f"Jikan timeout (attempt {attempt + 1})")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Jikan request error: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    
    return []


def batch_check_anime_in_db(mal_ids):
    """
    OPTIMIZED: Check multiple anime IDs in a single database query
    Returns a set of MAL IDs that exist in the database
    """
    if not mal_ids:
        return set()
    
    try:
        from app.database import query_db
        
        # Use a single query with IN clause
        placeholders = ','.join(['%s'] * len(mal_ids))
        query = f"SELECT mal_id FROM anime WHERE mal_id IN ({placeholders})"
        
        results = query_db(query, tuple(mal_ids))
        
        # Return a set of existing MAL IDs for O(1) lookup
        return {row['mal_id'] for row in results}
        
    except Exception as e:
        current_app.logger.error(f"Database batch check error: {e}")
        return set()


@jikan_bp.route('/search', methods=['GET'])
def api_jikan_search():
    """Search anime on Jikan API"""
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 10, type=int)
        
        current_app.logger.info(f"Jikan search: '{query}' (limit: {limit})")
        
        if not query or len(query) < 2:
            return jsonify({
                'success': False,
                'error': 'Query must be at least 2 characters'
            }), 400
        
        if limit > 25:
            limit = 25
        if limit < 1:
            limit = 10
        
        # Search Jikan API
        results = search_jikan_anime(query, limit)
        
        if not results:
            return jsonify({
                'success': True,
                'count': 0,
                'results': [],
                'message': 'No results found'
            })
        
        # OPTIMIZED: Batch check all MAL IDs in one query
        mal_ids = [anime.get('mal_id') for anime in results if anime.get('mal_id')]
        existing_mal_ids = batch_check_anime_in_db(mal_ids)
        
        # Format results
        formatted_results = []
        for anime in results:
            mal_id = anime.get('mal_id')
            if not mal_id:
                continue
                
            images = anime.get('images', {}).get('jpg', {})
            synopsis = anime.get('synopsis')
            
            formatted_results.append({
                'mal_id': mal_id,
                'title': anime.get('title'),
                'title_english': anime.get('title_english'),
                'type': anime.get('type'),
                'episodes': anime.get('episodes'),
                'score': anime.get('score'),
                'image_url': images.get('image_url') or images.get('large_image_url'),
                'synopsis': synopsis[:200] + '...' if synopsis and len(synopsis) > 200 else synopsis,
                'in_database': mal_id in existing_mal_ids  # O(1) lookup
            })
        
        current_app.logger.info(f"Jikan returned {len(formatted_results)} results")
        
        return jsonify({
            'success': True,
            'count': len(formatted_results),
            'results': formatted_results
        })
    
    except Exception as e:
        current_app.logger.error(f"Jikan search error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@jikan_bp.route('/import', methods=['POST'])
def api_jikan_import():
    """Import anime from Jikan to database"""
    try:
        data = request.get_json()
        
        if not data or 'mal_id' not in data:
            return jsonify({'error': 'mal_id required'}), 400
        
        mal_id = data['mal_id']
        
        # Quick check if already exists
        from app.database import query_db
        existing = query_db(
            "SELECT anime_id FROM anime WHERE mal_id = %s",
            (mal_id,),
            one=True
        )
        
        if existing:
            return jsonify({
                'success': False,
                'message': 'Anime already in database',
                'anime_id': existing['anime_id']
            }), 409
        
        # Fetch full details from Jikan
        url = f"{JIKAN_BASE_URL}/anime/{mal_id}/full"
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url, timeout=REQUEST_TIMEOUT)
                
                if response.status_code == 200:
                    break
                elif response.status_code == 429:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    current_app.logger.error(f"Jikan import error: {response.status_code}")
                    if attempt == MAX_RETRIES - 1:
                        return jsonify({'error': 'Failed to fetch from Jikan'}), 500
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    raise e
                time.sleep(RETRY_DELAY)
        
        anime_data = response.json().get('data')
        
        if not anime_data:
            return jsonify({'error': 'Anime not found'}), 404
        
        # Import to database
        from app.database import execute_db, query_db
        
        # Parse aired dates
        aired = anime_data.get('aired', {})
        aired_from = aired.get('from')[:10] if aired.get('from') else None
        aired_to = aired.get('to')[:10] if aired.get('to') else None
        
        # Get images
        images = anime_data.get('images', {})
        image_url = (
            images.get('jpg', {}).get('large_image_url') or 
            images.get('jpg', {}).get('image_url')
        )
        
        # Insert anime
        result = execute_db("""
            INSERT INTO anime (
                mal_id, title, title_english, title_japanese,
                type, episodes, status, aired_from, aired_to,
                duration, rating, score, scored_by, rank, popularity,
                synopsis, background, season, year, image_url
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING anime_id
        """, (
            mal_id,
            anime_data.get('title'),
            anime_data.get('title_english'),
            anime_data.get('title_japanese'),
            anime_data.get('type'),
            anime_data.get('episodes'),
            anime_data.get('status'),
            aired_from,
            aired_to,
            anime_data.get('duration'),
            anime_data.get('rating'),
            anime_data.get('score'),
            anime_data.get('scored_by'),
            anime_data.get('rank'),
            anime_data.get('popularity'),
            anime_data.get('synopsis'),
            anime_data.get('background'),
            anime_data.get('season'),
            anime_data.get('year'),
            image_url
        ), fetch=True)
        
        if not result:
            return jsonify({'error': 'Failed to import anime'}), 500
            
        anime_id = result[0]['anime_id']
        
        # Import genres
        genres = anime_data.get('genres', [])
        for genre in genres:
            genre_name = genre.get('name')
            if not genre_name:
                continue
                
            # Get or create genre
            genre_result = query_db(
                "SELECT genre_id FROM genres WHERE name = %s",
                (genre_name,),
                one=True
            )
            
            if genre_result:
                genre_id = genre_result['genre_id']
            else:
                genre_insert = execute_db(
                    "INSERT INTO genres (name) VALUES (%s) RETURNING genre_id",
                    (genre_name,),
                    fetch=True
                )
                genre_id = genre_insert[0]['genre_id'] if genre_insert else None
            
            if genre_id:
                # Link to anime
                execute_db(
                    """INSERT INTO anime_genres (anime_id, genre_id) 
                       VALUES (%s, %s) ON CONFLICT DO NOTHING""",
                    (anime_id, genre_id)
                )
        
        # Import studios
        studios = anime_data.get('studios', [])
        for studio in studios:
            studio_name = studio.get('name')
            if not studio_name:
                continue
                
            studio_result = query_db(
                "SELECT studio_id FROM studios WHERE name = %s",
                (studio_name,),
                one=True
            )
            
            if studio_result:
                studio_id = studio_result['studio_id']
            else:
                studio_insert = execute_db(
                    "INSERT INTO studios (name) VALUES (%s) RETURNING studio_id",
                    (studio_name,),
                    fetch=True
                )
                studio_id = studio_insert[0]['studio_id'] if studio_insert else None
            
            if studio_id:
                execute_db(
                    """INSERT INTO anime_studios (anime_id, studio_id) 
                       VALUES (%s, %s) ON CONFLICT DO NOTHING""",
                    (anime_id, studio_id)
                )
        
        current_app.logger.info(f"Successfully imported anime: {anime_data.get('title')} (ID: {anime_id})")
        
        return jsonify({
            'success': True,
            'message': 'Anime imported successfully',
            'anime_id': anime_id,
            'title': anime_data.get('title')
        }), 201
    
    except Exception as e:
        current_app.logger.error(f"Import error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@jikan_bp.route('/check/<int:mal_id>', methods=['GET'])
def api_jikan_check(mal_id):
    """Check if anime exists in database by MAL ID"""
    try:
        from app.database import query_db
        
        result = query_db(
            "SELECT anime_id, title FROM anime WHERE mal_id = %s",
            (mal_id,),
            one=True
        )
        
        if result:
            return jsonify({
                'success': True,
                'anime_id': result['anime_id'],
                'title': result['title']
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Anime not found in database'
            }), 404
            
    except Exception as e:
        current_app.logger.error(f"Check error: {e}")
        return jsonify({'error': str(e)}), 500