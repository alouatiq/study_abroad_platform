from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, advisor, agent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Role-specific relationships
    student_applications = db.relationship('Application', backref='student', lazy=True,
                                         foreign_keys='Application.student_id')
    advisor_applications = db.relationship('Application', backref='advisor', lazy=True,
                                         foreign_keys='Application.advisor_id')
    agent_applications = db.relationship('Application', backref='agent', lazy=True,
                                         foreign_keys='Application.agent_id')
