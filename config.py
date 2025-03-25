import os

class Config:
    # Secret key for session, CSRF protection, etc.
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

    # Database URL (Render provides this in ENV)
    SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL', 'postgresql://renderuser:password@host:port/dbname')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session settings
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_NAME = 'session'

    # Optional: log all SQL queries (for debugging locally)
    SQLALCHEMY_ECHO = os.getenv('FLASK_ENV') != 'production'
