# Initialize SQLAlchemy instance for use across the app
from flask_sqlalchemy import SQLAlchemy

# This `db` object will be imported and used in models and app factory
db = SQLAlchemy()
