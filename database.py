import os
import sqlite3
import re

# Import psycopg2 conditionally so it doesn't break if not installed locally for SQLite users
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

DB_FILE = 'businesses.db'

def get_engine():
    """Returns 'postgres' if DATABASE_URL is set, otherwise 'sqlite'"""
    if os.environ.get('DATABASE_URL'):
        return 'postgres'
    return 'sqlite'

def get_connection():
    """Returns a database connection object based on environment"""
    engine = get_engine()
    
    if engine == 'postgres':
        if not PSYCOPG2_AVAILABLE:
            raise ImportError("psycopg2-binary is required for PostgreSQL connections")
        
        conn = psycopg2.connect(
            os.environ.get('DATABASE_URL'),
            cursor_factory=RealDictCursor
        )
        return conn
    else:
        # SQLite fallback
        # Check if we are checking for Render persistent disk path
        db_path = DB_FILE
        if os.path.exists('/var/lib/data'):
            db_path = '/var/lib/data/businesses.db'
            
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

def prepare_query(sql):
    """
    Converts SQLite syntax (?) to Postgres syntax (%s) if needed.
    """
    if get_engine() == 'postgres':
        # Replace ? with %s
        return sql.replace('?', '%s')
    return sql

def init_tables(conn):
    """Creates the necessary tables if they don't exist"""
    cursor = conn.cursor()
    engine = get_engine()
    
    # Drop table if exists to ensure clean state (optional, maybe dangerous? keeping simple for now)
    # Actually, for init script, we usually want CREATE IF NOT EXISTS or explicit Recreation
    # Let's use CREATE IF NOT EXISTS
    
    if engine == 'postgres':
        # Postgres DDL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS businesses (
                id SERIAL PRIMARY KEY,
                name TEXT,
                address TEXT,
                city TEXT,
                zipCode TEXT,
                lat REAL,
                lng REAL,
                type TEXT,
                customerStatus TEXT,
                interactionCount INTEGER,
                lastVisit TEXT,
                priority TEXT,
                phone TEXT,
                contacts TEXT,
                visits TEXT
            )
        ''')
    else:
        # SQLite DDL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY,
                name TEXT,
                address TEXT,
                city TEXT,
                zipCode TEXT,
                lat REAL,
                lng REAL,
                type TEXT,
                customerStatus TEXT,
                interactionCount INTEGER,
                lastVisit TEXT,
                priority TEXT,
                phone TEXT,
                contacts TEXT,
                visits TEXT
            )
        ''')
    
    conn.commit()

def execute_insert_returning_id(cursor, sql, params):
    """
    Executes an INSERT and returns the new ID, handling driver differences.
    """
    engine = get_engine()
    
    if engine == 'postgres':
        # Use existing prepare_query logic or do it manually here
        sql = sql.replace('?', '%s')
        sql += " RETURNING id"
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return row['id']
    else:
        cursor.execute(sql, params)
        return cursor.lastrowid
