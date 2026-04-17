"""
Watchlist API routes for CRUD operations
"""
from flask import Blueprint, request, jsonify
from app.database import query_db, execute_db
from datetime import datetime

# Create blueprint
watchlist_bp = Blueprint('watchlist', __name__)


@watchlist_bp.route('/api/watchlist/<int:list_id>')
def get_watchlist_item(list_id):
    """
    GET single watchlist item by list_id
    Used by the edit modal to populate current values
    """
    try:
        # For now using hardcoded user_id = 1 (will use session in Week 3)
        user_id = 1
        
        item = query_db("""
            SELECT 
                ual.list_id, ual.watch_status, ual.user_score,
                ual.episodes_watched, ual.start_date, ual.finish_date,
                ual.notes,
                a.anime_id, a.title, a.episodes
            FROM user_anime_list ual
            JOIN anime a ON ual.anime_id = a.anime_id
            WHERE ual.list_id = %s AND ual.user_id = %s
        """, (list_id, user_id), one=True)
        
        if not item:
            return jsonify({'error': 'Watchlist item not found'}), 404
        
        # Convert dates to strings for JSON serialization
        result = dict(item)
        if result.get('start_date'):
            result['start_date'] = result['start_date'].isoformat()
        if result.get('finish_date'):
            result['finish_date'] = result['finish_date'].isoformat()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@watchlist_bp.route('/api/watchlist/add', methods=['POST'])
def add_to_watchlist():
    """
    POST - Add anime to user's watchlist
    Expected JSON: {anime_id, watch_status, user_score?, episodes_watched?, notes?}
    """
    try:
        user_id = 1  # Hardcoded for now
        data = request.get_json()
        
        # Validate required fields
        if not data.get('anime_id'):
            return jsonify({'error': 'anime_id is required'}), 400
        
        anime_id = data.get('anime_id')
        watch_status = data.get('watch_status', 'Plan to Watch')
        user_score = data.get('user_score')
        episodes_watched = data.get('episodes_watched', 0)
        notes = data.get('notes', '')
        start_date = data.get('start_date')
        finish_date = data.get('finish_date')
        
        # Check if already in watchlist
        existing = query_db("""
            SELECT list_id FROM user_anime_list 
            WHERE user_id = %s AND anime_id = %s
        """, (user_id, anime_id), one=True)
        
        if existing:
            return jsonify({'error': 'Anime already in watchlist'}), 400
        
        # Insert into watchlist
        result = execute_db("""
            INSERT INTO user_anime_list 
            (user_id, anime_id, watch_status, user_score, episodes_watched, 
             notes, start_date, finish_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING list_id
        """, (user_id, anime_id, watch_status, user_score, episodes_watched, 
              notes, start_date, finish_date), fetch=True)
        
        if result:
            return jsonify({
                'success': True, 
                'message': 'Added to watchlist',
                'list_id': result[0]['list_id']
            }), 201
        else:
            return jsonify({'error': 'Failed to add to watchlist'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@watchlist_bp.route('/api/watchlist/update', methods=['POST'])
def update_watchlist():
    """
    POST - Update existing watchlist entry
    Expected JSON: {list_id, watch_status, user_score?, episodes_watched?, notes?}
    """
    try:
        user_id = 1  # Hardcoded for now
        data = request.get_json()
        
        # Validate required fields
        if not data.get('list_id'):
            return jsonify({'error': 'list_id is required'}), 400
        
        list_id = data.get('list_id')
        watch_status = data.get('watch_status')
        user_score = data.get('user_score')
        episodes_watched = data.get('episodes_watched', 0)
        notes = data.get('notes', '')
        start_date = data.get('start_date')
        finish_date = data.get('finish_date')
        
        # Verify ownership
        existing = query_db("""
            SELECT list_id FROM user_anime_list 
            WHERE list_id = %s AND user_id = %s
        """, (list_id, user_id), one=True)
        
        if not existing:
            return jsonify({'error': 'Watchlist item not found or unauthorized'}), 404
        
        # Update watchlist entry
        rows_affected = execute_db("""
            UPDATE user_anime_list
            SET watch_status = %s,
                user_score = %s,
                episodes_watched = %s,
                notes = %s,
                start_date = %s,
                finish_date = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE list_id = %s AND user_id = %s
        """, (watch_status, user_score, episodes_watched, notes, 
              start_date, finish_date, list_id, user_id))
        
        if rows_affected > 0:
            return jsonify({
                'success': True,
                'message': 'Watchlist updated successfully'
            }), 200
        else:
            return jsonify({'error': 'No changes made'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@watchlist_bp.route('/api/watchlist/remove/<int:list_id>', methods=['DELETE'])
def remove_from_watchlist(list_id):
    """
    DELETE - Remove anime from watchlist
    """
    try:
        user_id = 1  # Hardcoded for now
        
        # Verify ownership before deleting
        existing = query_db("""
            SELECT list_id FROM user_anime_list 
            WHERE list_id = %s AND user_id = %s
        """, (list_id, user_id), one=True)
        
        if not existing:
            return jsonify({'error': 'Watchlist item not found or unauthorized'}), 404
        
        # Delete the entry
        rows_affected = execute_db("""
            DELETE FROM user_anime_list
            WHERE list_id = %s AND user_id = %s
        """, (list_id, user_id))
        
        if rows_affected > 0:
            return jsonify({
                'success': True,
                'message': 'Removed from watchlist'
            }), 200
        else:
            return jsonify({'error': 'Failed to remove from watchlist'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500