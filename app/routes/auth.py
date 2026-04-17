"""------------------
Simple session-based authentication routes.

Requires:
    pip install werkzeug   (already a Flask dependency, no extra install needed)

Add to app/__init__.py:
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

Set in your .env / config.py:
    SECRET_KEY = 'your-secret-key-here'   (Flask needs this for sessions)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import query_db, execute_db
from functools import wraps

auth_bp = Blueprint('auth', __name__)


# ============================================================
# LOGIN
# ============================================================

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Already logged in → go home
    if session.get('user_id'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')

        # Fetch user from DB
        user = query_db(
            "SELECT user_id, username, password_hash FROM users WHERE username = %s",
            (username,),
            one=True
        )

        if user and check_password_hash(user['password_hash'], password):
            # Store user info in session
            session['user_id'] = user['user_id']
            session['username'] = user['username']

            # Update last_login timestamp
            execute_db(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = %s",
                (user['user_id'],)
            )

            flash(f"Welcome back, {user['username']}!", 'success')
            # Redirect to the page they were trying to visit, or home
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Invalid username or password.', 'error')

# GET REQUEST → SHOW LOGIN FORM
    return render_template('login.html')


# ============================================================
# REGISTER
# ============================================================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        # --- Basic validation ---
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('register.html')

        # --- Check for duplicate username / email ---
        existing = query_db(
            "SELECT user_id FROM users WHERE username = %s OR email = %s",
            (username, email),
            one=True
        )
        if existing:
            flash('Username or email already in use.', 'error')
            return render_template('register.html')

        # --- Insert new user ---
        password_hash = generate_password_hash(password)
        result = execute_db(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING user_id
            """,
            (username, email, password_hash),
            fetch=True
        )

        if result:
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Something went wrong. Please try again.', 'error')

    return render_template('register.html')


# ============================================================
# LOGOUT
# ============================================================

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
