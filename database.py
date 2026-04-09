"""
Database connection and helper functions
"""
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from flask import current_app, g
from contextlib import contextmanager


class Database:
    """Database connection manager using connection pooling"""
    
    def __init__(self):
        self.connection_pool = None
    
    def init_app(self, app):
        """Initialize database connection pool with Flask app"""
        try:
            # Use ThreadedConnectionPool for better concurrency
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                1,  # Minimum connections
                20,  # Maximum connections
                host=app.config['DB_HOST'],
                port=app.config['DB_PORT'],
                database=app.config['DB_NAME'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD'],
                cursor_factory=RealDictCursor  # Set default cursor factory
            )
            app.logger.info("Database connection pool created successfully")
        except Exception as e:
            app.logger.error(f"Error creating connection pool: {e}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        if self.connection_pool:
            return self.connection_pool.getconn()
        raise Exception("Connection pool not initialized")
    
    def return_connection(self, conn):
        """Return connection to the pool"""
        if self.connection_pool:
            self.connection_pool.putconn(conn)
    
    def close_all_connections(self):
        """Close all connections in the pool"""
        if self.connection_pool:
            self.connection_pool.closeall()
    
    @contextmanager
    def get_cursor(self, commit=False):
        """
        Context manager for database cursor
        Usage:
            with db.get_cursor() as cursor:
                cursor.execute("SELECT * FROM anime")
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            self.return_connection(conn)


# Global database instance
db = Database()


def get_db():
    """
    Get database connection for current request context
    Stores connection in Flask's g object for reuse during request
    """
    if 'db_conn' not in g:
        g.db_conn = db.get_connection()
    return g.db_conn


def close_db(e=None):
    """Close database connection at end of request"""
    conn = g.pop('db_conn', None)
    if conn is not None:
        db.return_connection(conn)


def query_db(query, args=(), one=False, commit=False):
    """
    Execute a database query and return results
    
    Args:
        query: SQL query string
        args: Query parameters (tuple or dict)
        one: If True, return single row instead of list
        commit: If True, commit the transaction
    
    Returns:
        Query results as list of dictionaries or single dictionary if one=True
    """
    conn = get_db()
    cur = conn.cursor()  # Cursor factory already set in connection
    
    try:
        cur.execute(query, args)
        
        if commit:
            conn.commit()
            return cur.rowcount
        
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv
    
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Database query error: {e}")
        current_app.logger.error(f"Query: {query}")
        current_app.logger.error(f"Args: {args}")
        raise
    finally:
        cur.close()


def execute_db(query, args=(), fetch=False):
    """
    Execute a database query (INSERT, UPDATE, DELETE)
    
    Args:
        query: SQL query string
        args: Query parameters (tuple or dict)
        fetch: If True, return inserted/updated rows (use RETURNING clause)
    
    Returns:
        Number of affected rows or fetched rows if fetch=True
    """
    conn = get_db()
    cur = conn.cursor()
    
    try:
        cur.execute(query, args)
        conn.commit()
        
        if fetch:
            return cur.fetchall()
        
        return cur.rowcount
    
    except psycopg2.IntegrityError as e:
        conn.rollback()
        current_app.logger.error(f"Integrity error: {e}")
        raise ValueError("Duplicate entry or constraint violation") from e
    
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Database execution error: {e}")
        current_app.logger.error(f"Query: {query}")
        current_app.logger.error(f"Args: {args}")
        raise
    finally:
        cur.close()


def query_one(query, args=()):
    """Convenience function to fetch single row"""
    return query_db(query, args, one=True)


def query_all(query, args=()):
    """Convenience function to fetch all rows"""
    return query_db(query, args, one=False)


def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)
    
    # Register teardown function
    app.teardown_appcontext(close_db)
    
    # Optional: Test connection on startup
    with app.app_context():
        try:
            result = query_one("SELECT 1 as test")
            app.logger.info("Database connection test successful")
        except Exception as e:
            app.logger.error(f"Database connection test failed: {e}")
            raise