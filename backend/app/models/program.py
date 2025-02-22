from app import db

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    university = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    field_of_study = db.Column(db.String(100), nullable=False)
    tuition_fee = db.Column(db.Float, nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    language_requirement = db.Column(db.String(100))
    description = db.Column(db.Text)
    eligibility_criteria = db.Column(db.Text)
    available_scholarships = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    applications = db.relationship('Application', backref='program', lazy=True)
