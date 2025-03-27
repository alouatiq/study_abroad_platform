import os

class Config:
    # Secret key for session encryption, CSRF protection, etc.
    # Falls back to a default if not provided in environment
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

    # Main database connection URI (for PostgreSQL)
    # Use environment variable or fallback to local Render-style URI
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://renderuser:password@host:port/dbname'
    )

    # Disable event system to reduce overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_NAME = 'session'

    # Log all SQL queries in non-production environments (for debugging)
    SQLALCHEMY_ECHO = os.getenv('FLASK_ENV') != 'production'
