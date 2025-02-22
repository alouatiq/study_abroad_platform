from app import create_app, db
from app.models.user import User
from app.models.program import Program
from app.models.application import Application, Document, Message
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Add sample programs
        programs = [
            Program(
                name='Computer Science BSc',
                university='Technical University of Munich',
                country='Germany',
                field_of_study='Computer Science',
                tuition_fee=5000,
                duration_months=36,
                language_requirement='German B2',
                description='Leading computer science program in Germany',
                eligibility_criteria='High school diploma, German language proficiency',
                available_scholarships='DAAD Scholarship available'
            ),
            Program(
                name='Business Administration MBA',
                university='HEC Paris',
                country='France',
                field_of_study='Business',
                tuition_fee=9000,
                duration_months=24,
                language_requirement='English C1',
                description='Top-ranked MBA program in Europe',
                eligibility_criteria='Bachelor degree, 3 years work experience',
                available_scholarships='Merit-based scholarships available'
            )
        ]
        
        for program in programs:
            db.session.add(program)
        
        # Add sample users
        users = [
            User(
                email='student@example.com',
                password_hash=generate_password_hash('password'),
                role='student'
            ),
            User(
                email='advisor@example.com',
                password_hash=generate_password_hash('password'),
                role='advisor'
            ),
            User(
                email='agent@example.com',
                password_hash=generate_password_hash('password'),
                role='agent'
            )
        ]
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
