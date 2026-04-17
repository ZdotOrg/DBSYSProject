"""
Watchlist API routes for CRUD operations
"""
from flask import Blueprint, request, jsonify, session
from app.database import query_db, execute_db
from datetime import datetime
from functools import wraps

# Create blueprint
watchlist_bp = Blueprint('watchlist', __name__)


# ============================================================
# AUTHENTICATION DECORATOR
# ============================================================

def login_required(f):
    """Decorator to require login for API routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


# ============================================================
# WATCHLIST STATUS CHECK (NEEDED FOR ANIME DETAIL PAGE)
# ============================================================

@watchlist_bp.route('/api/watchlist/status/<int:anime_id>')
@login_required
def get_watchlist_status(anime_id):
    """
    GET - Check if anime is in user's watchlist
    Used by anime detail page to show correct button state
    """
    try:
        user_id = session.get('user_id')
        
        result = query_db("""
            SELECT 
                list_id, watch_status, episodes_watched, user_score
            FROM user_anime_list 
            WHERE user_id = %s AND anime_id = %s
        """, (user_id, anime_id), one=True)
        
        if result:
            return jsonify({
                'in_watchlist': True,
                'list_id': result['list_id'],
                'status': result['watch_status'],
                'episodes_watched': result['episodes_watched'],
                'user_score': result['user_score']
            })
        else:
            return jsonify({'in_watchlist': False})
            
    except Exception as e:
        print(f"Error checking watchlist status: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================
# SIMPLE ADD/UPDATE (USED BY ANIME DETAIL PAGE BUTTON)
# ============================================================

@watchlist_bp.route('/api/watchlist/add', methods=['POST'])
@login_required
def add_to_watchlist_simple():
    """
    POST - Simple add/update from anime detail page
    Expected JSON: {anime_id, status?}
    If anime exists, updates status; if not, creates new entry
    """
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        
        # Validate required fields
        if not data.get('anime_id'):
            return jsonify({'success': False, 'error': 'anime_id is required'}), 400
        
        anime_id = data.get('anime_id')
        status = data.get('status', 'Plan to Watch')
        
        # Check if anime exists
        anime = query_db("SELECT anime_id FROM anime WHERE anime_id = %s", 
                        (anime_id,), one=True)
        if not anime:
            return jsonify({'success': False, 'error': 'Anime not found'}), 404
        
        # Check if already in watchlist
        existing = query_db("""
            SELECT list_id FROM user_anime_list 
            WHERE user_id = %s AND anime_id = %s
        """, (user_id, anime_id), one=True)
        
        if existing:
            # Update existing entry
            execute_db("""
                UPDATE user_anime_list 
                SET watch_status = %s, updated_at = NOW()
                WHERE user_id = %s AND anime_id = %s
            """, (status, user_id, anime_id))
            return jsonify({
                'success': True, 
                'message': 'Watchlist updated successfully',
                'action': 'updated'
            })
        else:
            # Insert new entry
            result = execute_db("""
                INSERT INTO user_anime_list (user_id, anime_id, watch_status, updated_at)
                VALUES (%s, %s, %s, NOW())
                RETURNING list_id
            """, (user_id, anime_id, status), fetch=True)
            
            return jsonify({
                'success': True, 
                'message': 'Added to watchlist successfully',
                'action': 'added',
                'list_id': result[0]['list_id'] if result else None
            }), 201
        
    except Exception as e:
        print(f"Error adding to watchlist: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# GET SINGLE WATCHLIST ITEM (FOR EDIT MODAL)
# ============================================================

@watchlist_bp.route('/api/watchlist/item/<int:list_id>')
@login_required
def get_watchlist_item(list_id):
    """
    GET single watchlist item by list_id
    Used by the edit modal to populate current values
    """
    try:
        user_id = session.get('user_id')
        
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
        print(f"Error getting watchlist item: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================
# DETAILED ADD (FOR WATCHLIST PAGE WITH ALL FIELDS)
# ============================================================

@watchlist_bp.route('/api/watchlist/add-detailed', methods=['POST'])
@login_required
def add_to_watchlist_detailed():
    """
    POST - Add anime with full details (from watchlist page)
    Expected JSON: {anime_id, watch_status, user_score?, episodes_watched?, notes?}
    """
    try:
        user_id = session.get('user_id')
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
        print(f"Error adding detailed watchlist item: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================
# UPDATE WATCHLIST ITEM
# ============================================================

@watchlist_bp.route('/api/watchlist/update', methods=['POST'])
@login_required
def update_watchlist():
    """
    POST - Update existing watchlist entry
    Expected JSON: {list_id, watch_status, user_score?, episodes_watched?, notes?}
    """
    try:
        user_id = session.get('user_id')
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
        print(f"Error updating watchlist: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================
# REMOVE FROM WATCHLIST
# ============================================================

@watchlist_bp.route('/api/watchlist/remove/<int:list_id>', methods=['DELETE'])
@login_required
def remove_from_watchlist(list_id):
    """
    DELETE - Remove anime from watchlist by list_id
    """
    try:
        user_id = session.get('user_id')
        
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
        print(f"Error removing from watchlist: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================
# REMOVE BY ANIME ID (FOR ANIME DETAIL PAGE)
# ============================================================

@watchlist_bp.route('/api/watchlist/remove-by-anime', methods=['POST'])
@login_required
def remove_by_anime_id():
    """
    POST - Remove anime from watchlist by anime_id
    Expected JSON: {anime_id}
    """
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        
        if not data.get('anime_id'):
            return jsonify({'success': False, 'error': 'anime_id is required'}), 400
        
        anime_id = data.get('anime_id')
        
        # Delete the entry
        rows_affected = execute_db("""
            DELETE FROM user_anime_list
            WHERE user_id = %s AND anime_id = %s
        """, (user_id, anime_id))
        
        if rows_affected > 0:
            return jsonify({
                'success': True,
                'message': 'Removed from watchlist'
            }), 200
        else:
            return jsonify({
                'success': False, 
                'error': 'Anime not in watchlist'
            }), 404
    
    except Exception as e:
        print(f"Error removing by anime ID: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500