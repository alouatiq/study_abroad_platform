import uuid
from datetime import datetime
from extensions import db  # SQLAlchemy instance from extensions.py

# Utility function to generate UUIDs for primary keys
def generate_uuid():
    return str(uuid.uuid4())


# -------------------------------
# Student Model
# -------------------------------
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone_number = db.Column(db.String(50))
    nationality = db.Column(db.String(100))
    country_of_residence = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------------------
# Agency Model
# -------------------------------
class Agency(db.Model):
    __tablename__ = 'agencies'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------------------
# Program Model
# -------------------------------
class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    agency_id = db.Column(db.String(36), db.ForeignKey('agencies.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    university = db.Column(db.String(255))
    field = db.Column(db.String(50), default="Unknown")
    country = db.Column(db.String(50))
    fee = db.Column(db.Numeric(10, 2))
    duration = db.Column(db.String(50))
    languages = db.Column(db.String(50), default="English")
    proficiency_level = db.Column(db.String(50), default="B2")
    eligibility_criteria = db.Column(db.String(255))
    available_scholarships = db.Column(db.Boolean())
    deadline = db.Column(db.DateTime)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to access agency from a program
    agency = db.relationship('Agency', backref='programs', lazy=True)


# -------------------------------
# Advisor Model
# -------------------------------
class Advisor(db.Model):
    __tablename__ = 'advisor'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    full_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(50))
    country_of_residence = db.Column(db.String(100))

    # NOTE: You can optionally link advisors to agencies or programs later
    # Uncomment below lines when needed
    # agency_id = db.Column(db.String(36), db.ForeignKey('agencies.id'))
    # program_id = db.Column(db.String(36), db.ForeignKey('programs.id'))


# -------------------------------
# StudentProgram Association Table
# -------------------------------
class StudentProgram(db.Model):
    __tablename__ = 'student_programs'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False)
    program_id = db.Column(db.String(36), db.ForeignKey('programs.id'), nullable=False)
    status = db.Column(db.String(50), default="pending")  # Status: pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student = db.relationship("Student", backref="student_programs")
    program = db.relationship("Program", backref="student_programs")


# -------------------------------
# AdvisorAssignment Table (Advisors assigned to students for a specific program)
# -------------------------------
class AdvisorAssignment(db.Model):
    __tablename__ = 'advisor_assignments'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    advisor_id = db.Column(db.String(36), db.ForeignKey('advisor.id'), nullable=False)
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False)
    program_id = db.Column(db.String(36), db.ForeignKey('programs.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    advisor = db.relationship("Advisor", backref="advisor_assignments")
    student = db.relationship("Student", backref="advisor_assignments")
    program = db.relationship("Program", backref="advisor_assignments")


# -------------------------------
# AdvisorApplication Table (Advisors applying to assist with a program)
# -------------------------------
class AdvisorApplication(db.Model):
    __tablename__ = 'advisor_applications'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    advisor_id = db.Column(db.String(36), db.ForeignKey('advisor.id'), nullable=False)
    program_id = db.Column(db.String(36), db.ForeignKey('programs.id'), nullable=False)
    assistance_approval = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    advisor = db.relationship("Advisor", backref="advisor_applications")
    program = db.relationship("Program", backref="advisor_applications")
