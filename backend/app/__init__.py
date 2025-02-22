from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    with app.app_context():
        # Initialize scheduler
        from app.tasks import init_scheduler
        init_scheduler()
        
        # Import models to register them with SQLAlchemy
        from app.models.user import User
        from app.models.program import Program
        from app.models.application import Application, Document, Message
        
        # Create all tables
        db.create_all()
        
        # Register blueprints
        from app.routes.main import bp as main_bp
        from app.routes.programs import bp as programs_bp
        from app.routes.applications import bp as applications_bp
        from app.routes.advisors import bp as advisors_bp
        from app.routes.agents import bp as agents_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(programs_bp)
        app.register_blueprint(applications_bp)
        app.register_blueprint(advisors_bp)
        app.register_blueprint(agents_bp)
    
    return app
