"""
Database connection and helper functions
"""
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from flask import current_app, g


class Database:
    """Database connection manager using connection pooling"""
    
    def __init__(self):
        self.connection_pool = None
    
    def init_app(self, app):
        """Initialize database connection pool with Flask app"""
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1,  # Minimum connections
                20,  # Maximum connections
                host=app.config['DB_HOST'],
                port=app.config['DB_PORT'],
                database=app.config['DB_NAME'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD']
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

            
    # explain this
    def query(self, sql, args=()):
        """Quick query method that handles connection lifecycle"""
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(sql, args)
            return cur.fetchall()
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Query error: {e}")
            raise
        finally:
            cur.close()
            self.return_connection(conn)
    
    # THIS TOO
    def query_one(self, sql, args=()):
        """Quick query for single row"""
        results = self.query(sql, args)
        return results[0] if results else None


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
        args: Query parameters (tuple)
        one: If True, return single row instead of list
        commit: If True, commit the transaction
    
    Returns:
        Query results as list of dictionaries or single dictionary if one=True
    """
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute(query, args)
        
        if commit:
            conn.commit()
            return cur.rowcount
        
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Database query error: {e}")
        raise
    finally:
        cur.close()


def execute_db(query, args=(), fetch=False):
    """
    Execute a database query (INSERT, UPDATE, DELETE)
    
    Args:
        query: SQL query string
        args: Query parameters (tuple)
        fetch: If True, return inserted/updated rows
    
    Returns:
        Number of affected rows or fetched rows if fetch=True
    """
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute(query, args)
        conn.commit()
        
        if fetch:
            rv = cur.fetchall()
            cur.close()
            return rv
        
        rowcount = cur.rowcount
        cur.close()
        return rowcount
    
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Database execution error: {e}")
        raise
    finally:
        cur.close()


def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)
    
    # Register teardown function
    app.teardown_appcontext(close_db)