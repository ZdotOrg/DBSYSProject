"""
Main application routes
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from app.database import query_db, execute_db
from functools import wraps

# AUTHENTICATION DECORATOR

def login_required(f):
    """Decorator to require login for certain routes"""
   
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# Create blueprint
main_bp = Blueprint('main', __name__)

# READ OPERATION
@main_bp.route('/')
def index():
    """Home page - displays featured/popular anime"""
    try:
        # Get top 12 anime by score for homepage
        anime_list = query_db("""
            SELECT 
                anime_id, mal_id, title, title_english, 
                type, episodes, score, image_url, synopsis
            FROM anime
            WHERE score IS NOT NULL
            ORDER BY score DESC, popularity ASC
            LIMIT 12
        """)
        
        return render_template('index.html', anime_list=anime_list)
    
    except Exception as e:
        print(f"Error loading home page: {e}")
        return render_template('index.html', anime_list=[], error=str(e))


#READ OPERATION
@main_bp.route('/search')
def search():
    """Search page - search anime by title, genre, etc."""
    try:
        # Get search query from URL parameters
        search_query = request.args.get('q', '').strip()
        genre_filter = request.args.get('genre', '')
        type_filter = request.args.get('type', '')
        status_filter = request.args.get('status', '')
        sort_by = request.args.get('sort', 'score_desc')
        
        # Base query
        query = """
            SELECT DISTINCT
                a.anime_id, a.mal_id, a.title, a.title_english,
                a.type, a.episodes, a.score, a.image_url, a.synopsis,
                a.status, a.year
            FROM anime a
            LEFT JOIN anime_genres ag ON a.anime_id = ag.anime_id
            LEFT JOIN genres g ON ag.genre_id = g.genre_id
            WHERE 1=1
        """
        
        params = []
        
        # Add search filter
        if search_query:
            query += " AND (LOWER(a.title) LIKE LOWER(%s) OR LOWER(a.title_english) LIKE LOWER(%s))"
            params.extend([f"%{search_query}%", f"%{search_query}%"])
        
        # Add genre filter
        if genre_filter:
            query += " AND g.name = %s"
            params.append(genre_filter)
        
        # Add type filter
        if type_filter:
            query += " AND a.type = %s"
            params.append(type_filter)
        
        # Add status filter
        if status_filter:
            query += " AND a.status = %s"
            params.append(status_filter)
        
        # Add sorting
        if sort_by == 'score_desc':
            query += " ORDER BY a.score DESC NULLS LAST"
        elif sort_by == 'score_asc':
            query += " ORDER BY a.score ASC NULLS LAST"
        elif sort_by == 'title_asc':
            query += " ORDER BY a.title ASC"
        elif sort_by == 'popularity':
            query += " ORDER BY a.popularity ASC"
        else:
            query += " ORDER BY a.score DESC NULLS LAST"
        
        query += " LIMIT 50"
        
        # Execute query
        results = query_db(query, tuple(params))
        
        # Get all genres for filter dropdown
        genres = query_db("SELECT DISTINCT name FROM genres ORDER BY name")
        
        # Get all types for filter dropdown
        types = query_db("SELECT DISTINCT type FROM anime WHERE type IS NOT NULL ORDER BY type")
        
        # Get all statuses for filter dropdown
        statuses = query_db("SELECT DISTINCT status FROM anime WHERE status IS NOT NULL ORDER BY status")
        
        # Calculate result count
        result_count = len(results)
        
        return render_template('search.html', 
                             results=results,
                             genres=genres,
                             types=types,
                             statuses=statuses,
                             search_query=search_query,
                             selected_genre=genre_filter,
                             selected_type=type_filter,
                             selected_status=status_filter,
                             selected_sort=sort_by,
                             result_count=result_count)
    
    except Exception as e:
        print(f"Error in search: {e}")
        return render_template('search.html', 
                             results=[], 
                             genres=[],
                             types=[],
                             statuses=[],
                             result_count=0,
                             error=str(e))


# READ OPERATION
@main_bp.route('/watchlist')
def watchlist():
    """Watchlist page - displays user's anime list"""
    try:
        # For now, using a hardcoded test user (user_id = 1)
        # In Week 3, this will use session/authentication
                # Get user_id from session
        user_id = session.get('user_id')
        
        if not user_id:
            flash('Please log in to view your watchlist.', 'warning')
            return redirect(url_for('auth.login'))
        # Get user's watchlist with anime details
        watchlist_items = query_db("""
            SELECT 
                ual.list_id, ual.watch_status, ual.user_score,
                ual.episodes_watched, ual.start_date, ual.finish_date,
                ual.notes, ual.updated_at,
                a.anime_id, a.mal_id, a.title, a.title_english,
                a.type, a.episodes, a.score, a.image_url, a.synopsis
            FROM user_anime_list ual
            JOIN anime a ON ual.anime_id = a.anime_id
            WHERE ual.user_id = %s
            ORDER BY ual.updated_at DESC
        """, (user_id,))
        
        # Group by watch status
        watching = [item for item in watchlist_items if item['watch_status'] == 'Watching']
        completed = [item for item in watchlist_items if item['watch_status'] == 'Completed']
        plan_to_watch = [item for item in watchlist_items if item['watch_status'] == 'Plan to Watch']
        on_hold = [item for item in watchlist_items if item['watch_status'] == 'On Hold']
        dropped = [item for item in watchlist_items if item['watch_status'] == 'Dropped']
        
        return render_template('watchlist.html',
                             watching=watching,
                             completed=completed,
                             plan_to_watch=plan_to_watch,
                             on_hold=on_hold,
                             dropped=dropped,
                             total_count=len(watchlist_items))
    
    except Exception as e:
        print(f"Error loading watchlist: {e}")
        return render_template('watchlist.html', 
                             watching=[],
                             completed=[],
                             plan_to_watch=[],
                             on_hold=[],
                             dropped=[],
                             total_count=0,
                             error=str(e))


# READ OPERATION 
@main_bp.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    """Anime detail page"""
    try:
        # Get anime details
        anime = query_db("""
            SELECT *
            FROM anime
            WHERE anime_id = %s
        """, (anime_id,), one=True)
        
        if not anime:
            return "Anime not found", 404
        
        # Get genres
        genres = query_db("""
            SELECT g.name
            FROM genres g
            JOIN anime_genres ag ON g.genre_id = ag.genre_id
            WHERE ag.anime_id = %s
        """, (anime_id,))
        
        # Get themes
        themes = query_db("""
            SELECT t.name
            FROM themes t
            JOIN anime_themes at ON t.theme_id = at.theme_id
            WHERE at.anime_id = %s
        """, (anime_id,))
        
        # Get studios
        studios = query_db("""
            SELECT s.name
            FROM studios s
            JOIN anime_studios ast ON s.studio_id = ast.studio_id
            WHERE ast.anime_id = %s
        """, (anime_id,))
        
        return render_template('anime_detail.html',
                             anime=anime,
                             genres=genres,
                             themes=themes,
                             studios=studios)
    
    except Exception as e:
        print(f"Error loading anime detail: {e}")
        return f"Error: {e}", 500


@main_bp.route('/recommendations')
def recommendations():
    """Recommendations page - personalized anime recommendations"""
    # Placeholder for Week 2-3 advanced algorithm
    return render_template('recommendations.html', recommendations=[])


# ============================================================
# API ROUTES (for AJAX requests)
# ============================================================


# READ OPERATION
@main_bp.route('/api/anime/<int:anime_id>')
def api_anime_detail(anime_id):
    """API endpoint to get anime details as JSON"""
    try:
        anime = query_db("""
            SELECT *
            FROM anime
            WHERE anime_id = %s
        """, (anime_id,), one=True)
        
        if not anime:
            return jsonify({'error': 'Anime not found'}), 404
        
        return jsonify(dict(anime))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# READ OPERATION
@main_bp.route('/api/search')
def api_search():
    """API endpoint for search suggestions"""
    try:
        query = request.args.get('q', '').strip()
        
        if len(query) < 2:
            return jsonify([])
        
        results = query_db("""
            SELECT anime_id, title, title_english, image_url
            FROM anime
            WHERE LOWER(title) LIKE LOWER(%s) OR LOWER(title_english) LIKE LOWER(%s)
            ORDER BY popularity ASC
            LIMIT 10
        """, (f"%{query}%", f"%{query}%"))
        
        return jsonify([dict(r) for r in results])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================
# ERROR HANDLERS
# ============================================================

@main_bp.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return render_template('404.html'), 404


@main_bp.errorhandler(500)
def server_error(e):
    """500 error handler"""
    return render_template('500.html'), 500