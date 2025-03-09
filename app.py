from models import Student, Agency, Program, Advisor, StudentProgram, AdvisorAssignment
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from config import Config
from datetime import datetime
import uuid
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from forms import StudentRegistrationForm, StudentLoginForm, AgencyRegistrationForm, AgencyLoginForm, AdvisorRegistrationForm, AdvisorLoginForm

# Import the db from the extensions module
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database with the app
db.init_app(app)
migrate = Migrate(app, db)
Session(app)

# Import models after initializing the db

# Helper function to generate a UUID


def generate_uuid():
    return str(uuid.uuid4())


def is_logged_in(role, user_id):
    return session.get(role) == user_id

# -------------------------
# Routes
# -------------------------


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/programs')
def programs():
    return render_template("programs.html")



@app.route('/api/programs', methods=['GET'])
def api_programs():
    fee = request.args.get('fee')
    country = request.args.get('country')
    field = request.args.get('field')
    university = request.args.get('university')

    query = Program.query
    if fee:
        query = query.filter(Program.fee <= fee)
    if country:
        query = query.filter(Program.country.ilike(f'%{country}%'))
    if field:
        query = query.filter(Program.field.ilike(f'%{field}%'))
    if university:
        query = query.filter(Program.university.ilike(f'%{university}%'))

    programs_list = query.all()
    data = [{
        'id': p.id,
        'name': p.name,
        'university': p.university,
        'field': p.field,
        'country': p.country,
        'fee': float(p.fee) if p.fee else 0,
        'deadline': p.deadline.strftime('%Y-%m-%d') if p.deadline else None,
    } for p in programs_list]
    return jsonify(data)


@app.route('/api/advisors')
def api_advisors():
    program_name = request.args.get('program_name', '')
    country = request.args.get('country', '')
    university = request.args.get('university', '')
    
    # Perform an outer join with Program (if an advisor has chosen a program)
    query = Advisor.query.outerjoin(Program, Advisor.program_id == Program.id)
    
    if program_name:
        query = query.filter(Program.name.ilike(f'%{program_name}%'))
    if country:
        query = query.filter(Advisor.country_of_residence.ilike(f'%{country}%'))
    if university:
        query = query.filter(Program.university.ilike(f'%{university}%'))
    
    advisors = query.all()
    data = []
    for advisor in advisors:
        if advisor.program_id:
            program = Program.query.get(advisor.program_id)
            program_university = program.university if program else None
            program_name_val = program.name if program else None
        else:
            program_university = None
            program_name_val = None
        # Build list of assisted student names from AdvisorAssignment model
        assignments = AdvisorAssignment.query.filter_by(advisor_id=advisor.id).all()
        assisted_students = []
        for assignment in assignments:
            student = Student.query.get(assignment.student_id)
            if student:
                assisted_students.append(student.full_name)
        data.append({
            'id': advisor.id,
            'full_name': advisor.full_name,
            'country_of_residence': advisor.country_of_residence,
            'program_university': program_university,
            'program_name': program_name_val,
            'assisted_students': assisted_students,
        })
    return jsonify(data)

@app.route('/programs/<program_id>')
def program_detail(program_id):
    program = Program.query.get_or_404(program_id)
    return render_template('program_detail.html', program=program)


@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        full_name = form.full_name.data
        password = generate_password_hash(form.password.data)

        if Student.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for('register_student'))

        new_student = Student(
            id=generate_uuid(),
            email=email,
            full_name=full_name,
            password=password
        )
        db.session.add(new_student)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for('login_student'))
    return render_template('register_student.html', form=form)


@app.route('/login/student', methods=['GET', 'POST'])
def login_student():
    form = StudentLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        student = Student.query.filter_by(email=email).first()
        if student and check_password_hash(student.password, password):
            session['student'] = student.id
            flash("Logged in successfully", "success")
            return redirect(url_for('student_dashboard', student_id=student.id))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for('login_student'))
    return render_template('login_student.html', form=form)


@app.route('/students/<student_id>/dashboard')
def student_dashboard(student_id):
    if not is_logged_in('student', student_id):
        flash("You need to be logged in as a student", "warning")
        return redirect(url_for('login_student'))
    student = Student.query.get_or_404(student_id)
    applications = StudentProgram.query.filter_by(student_id=student_id).all()
    return render_template('student_dashboard.html', student=student, applications=applications)


@app.route('/students/<student_id>/apply/<program_id>', methods=['POST'])
def apply_to_program(student_id, program_id):
    if not is_logged_in('student', student_id):
        flash("You need to be logged in to apply", "warning")
        return redirect(url_for('login_student'))

    existing_application = StudentProgram.query.filter_by(
        student_id=student_id, program_id=program_id).first()
    if existing_application:
        flash("You have already applied to this program", "warning")
        return redirect(url_for('student_dashboard', student_id=student_id))

    new_application = StudentProgram(
        id=generate_uuid(),
        student_id=student_id,
        program_id=program_id,
        created_at=datetime.utcnow()
    )

    db.session.add(new_application)
    db.session.commit()
    flash("Application submitted successfully", "success")

    return redirect(url_for('student_dashboard', student_id=student_id))


@app.route('/delete_application/<string:id>', methods=['POST'])
def delete_application(id):
    app = StudentProgram.query.get_or_404(id)
    # Assuming `student_id` is a field in the application model
    student_id = app.student_id
    db.session.delete(app)
    db.session.commit()
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('student_dashboard', student_id=student_id))


@app.route('/students/<student_id>/dashboard/documents', methods=['GET', 'POST'])
def student_documents(student_id):
    if not is_logged_in('student', student_id):
        flash("Please login to access your documents", "warning")
        return redirect(url_for('login_student'))
    if request.method == 'POST':
        # File handling logic here
        flash("Documents updated", "success")
        return redirect(url_for('student_documents', student_id=student_id))
    return render_template('student_documents.html')


@app.route('/students/<student_id>/profile', methods=['GET', 'POST'])
def student_profile(student_id):
    if not is_logged_in('student', student_id):
        flash("Please login to access your profile", "warning")
        return redirect(url_for('login_student'))
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.full_name = request.form.get('full_name')
        # Update additional fields as needed
        db.session.commit()
        flash("Profile updated", "success")
        return redirect(url_for('student_profile', student_id=student_id))
    return render_template('student_profile.html', student=student)


@app.route('/programs/<string:program_id>/edit', methods=['POST'])
def edit_program(program_id):
    program = Program.query.get_or_404(program_id)
    
    # Update fields from the modal form
    program.name = request.form.get('name')
    program.university = request.form.get('university')
    program.field = request.form.get('field')
    program.country = request.form.get('country')
    
    fee = request.form.get('fee')
    try:
        program.fee = float(fee) if fee else 0
    except ValueError:
        program.fee = 0

    deadline = request.form.get('deadline')
    if deadline:
        try:
            program.deadline = datetime.strptime(deadline, '%Y-%m-%d')
        except ValueError:
            program.deadline = None
    else:
        program.deadline = None

    program.description = request.form.get('description')
    
    db.session.commit()
    flash("Program updated successfully", "success")
    return redirect(url_for('agency_dashboard', agency_id=program.agency_id))

@app.route('/programs/<string:program_id>/delete', methods=['POST'])
def delete_program(program_id):
    program = Program.query.get_or_404(program_id)
    agency_id = program.agency_id
    db.session.delete(program)
    db.session.commit()
    flash("Program deleted successfully", "success")
    return redirect(url_for('agency_dashboard', agency_id=agency_id))

# --- Agency Routes ---


@app.route('/register/agency', methods=['GET', 'POST'])
def register_agency():
    form = AgencyRegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        password = generate_password_hash(form.password.data)

        if Agency.query.filter_by(name=name).first():
            flash("Agency already exists", "danger")
            return redirect(url_for('register_agency'))

        new_agency = Agency(
            id=generate_uuid(),
            name=name,
            password=password
        )
        db.session.add(new_agency)
        db.session.commit()
        flash("Agency registration successful. Please login.", "success")
        return redirect(url_for('login_agency'))
    return render_template('register_agency.html', form=form)


@app.route('/login/agency', methods=['GET', 'POST'])
def login_agency():
    form = AgencyLoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        agency = Agency.query.filter_by(name=name).first()
        if agency and check_password_hash(agency.password, password):
            session['agency'] = agency.id
            flash("Logged in successfully", "success")
            return redirect(url_for('agency_dashboard', agency_id=agency.id))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for('login_agency'))
    return render_template('login_agency.html', form=form)


@app.route('/agencies/<agency_id>/dashboard')
def agency_dashboard(agency_id):
    if session.get('agency') != agency_id:
        flash("Please login as agency", "warning")
        return redirect(url_for('login_agency'))

    agency = Agency.query.get_or_404(agency_id)
    programs = Program.query.filter_by(agency_id=agency_id).all()
    advisors = Advisor.query.filter_by(agency_id=agency_id).all()
    advisor_assignments = AdvisorAssignment.query.all()  # Fetch all assignments
    available_students = Student.query.all()  # Ideally, filter unassigned students

    return render_template(
        'agency_dashboard.html', agency=agency,
        programs=programs,
        advisors=advisors,
        available_students=available_students,
        advisor_assignments=advisor_assignments  # Pass this to template
    )


@app.route('/agencies/<agency_id>/dashboard/students')
def agency_students(agency_id):
    if session.get('agency') != agency_id:
        flash("Please login as agency", "warning")
        return redirect(url_for('login_agency'))
    return render_template('agency_students.html')


@app.route('/agencies/<string:agency_id>/dashboard/advisors')
def agency_advisors(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    advisors = Advisor.query.filter_by(agency_id=agency_id).all()
    programs = Program.query.filter_by(agency_id=agency_id).all()
    programs_dict = {p.id: p for p in programs}
    advisor_assignments = AdvisorAssignment.query.all()  # You may filter this further if needed.
    available_students = Student.query.all()  # Optionally, filter out already assigned students.
    return render_template('agency_advisors.html', 
                           agency=agency, 
                           advisors=advisors, 
                           programs=programs, 
                           programs_dict=programs_dict, 
                           advisor_assignments=advisor_assignments, 
                           available_students=available_students)



@app.route('/agencies/<agency_id>/dashboard/advisors/<advisor_id>/unassign/<student_id>', methods=['POST'])
def unassign_student(agency_id, advisor_id, student_id):
    if session.get('agency') != agency_id:
        flash("Please login as agency", "warning")
        return redirect(url_for('login_agency'))

    assignment = AdvisorAssignment.query.filter_by(
        advisor_id=advisor_id, student_id=student_id).first()
    if assignment:
        db.session.delete(assignment)
        db.session.commit()
        flash("Student unassigned successfully", "success")
    else:
        flash("Assignment not found", "danger")

    return redirect(url_for('agency_advisors', agency_id=agency_id))


@app.route('/agencies/<agency_id>/dashboard/advisors/<advisor_id>/assign', methods=['POST'])
def assign_advisor(agency_id, advisor_id):
    if session.get('agency') != agency_id:
        flash("Please login as agency", "warning")
        return redirect(url_for('login_agency'))

    student_id = request.form.get('student_id')

    if not student_id:
        flash("No student selected", "danger")
        return redirect(url_for('agency_advisors', agency_id=agency_id))

    # Check if the student is already assigned to any advisor
    existing_assignment = AdvisorAssignment.query.filter_by(
        student_id=student_id).first()
    if existing_assignment:
        flash("This student is already assigned to an advisor.", "warning")
        return redirect(url_for('agency_advisors', agency_id=agency_id))

    # Create a new advisor assignment record
    new_assignment = AdvisorAssignment(
        id=generate_uuid(),
        advisor_id=advisor_id,
        student_id=student_id
    )
    db.session.add(new_assignment)
    db.session.commit()

    flash("Advisor assigned to student successfully", "success")
    return redirect(url_for('agency_advisors', agency_id=agency_id))


@app.route('/agencies/<agency_id>/profile', methods=['GET', 'POST'])
def agency_profile(agency_id):
    if session.get('agency') != agency_id:
        flash("Please login as agency", "warning")
        return redirect(url_for('login_agency'))
    agency = Agency.query.get_or_404(agency_id)
    if request.method == 'POST':
        agency.name = request.form.get('name')
        db.session.commit()
        flash("Profile updated", "success")
        return redirect(url_for('agency_profile', agency_id=agency_id))
    return render_template('agency_profile.html', agency=agency)


@app.route('/agencies/<agency_id>/programs/new', methods=['GET', 'POST'])
def create_program(agency_id):
    # Ensure the agency is logged in
    if session.get('agency') != agency_id:
        flash("Please login as agency", "warning")
        return redirect(url_for('login_agency'))

    if request.method == 'POST':
        name = request.form.get('name')
        university = request.form.get('university')
        field = request.form.get('field')
        country = request.form.get('country')
        fee = request.form.get('fee')
        duration = request.form.get('duration')
        languages = request.form.get('languages')
        proficiency_level = request.form.get('proficiency_level')
        eligibility_criteria = request.form.get('eligibility_criteria')
        available_scholarships = request.form.get('available_scholarships')
        # Expecting a string in YYYY-MM-DD format
        deadline = request.form.get('deadline')
        description = request.form.get('description')

        # Basic backend validation
        if not name or not university:
            flash("Program Name and University are required", "danger")
            return redirect(url_for('create_program', agency_id=agency_id))

        # Convert fee and deadline if provided
        try:
            fee_val = float(fee) if fee else 0
        except ValueError:
            fee_val = 0

        try:
            deadline_dt = datetime.strptime(
                deadline, "%Y-%m-%d") if deadline else None
        except ValueError:
            deadline_dt = None

        new_program = Program(
            id=generate_uuid(),
            agency_id=agency_id,
            name=name,
            university=university,
            field=field,
            country=country,
            fee=fee_val,
            duration=duration,
            languages=languages,
            proficiency_level=proficiency_level,
            eligibility_criteria=eligibility_criteria,
            available_scholarships=available_scholarships,
            deadline=deadline_dt,
            description=description
        )
        db.session.add(new_program)
        db.session.commit()
        flash("Program created successfully", "success")
        return redirect(url_for('agency_dashboard', agency_id=agency_id))

    return render_template('create_program.html', agency_id=agency_id)

# --- Advisor Routes ---


@app.route('/register/advisor', methods=['GET', 'POST'])
def register_advisor():
    form = AdvisorRegistrationForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        # agency_id = form.agency_id.data
        # program_id = form.program_id.data
        country_of_residence = form.country_of_residence.data
        phone_number = form.phone_number.data

        new_advisor = Advisor(
            id=generate_uuid(),
            full_name=full_name,
            email=email,
            password=password,
            country_of_residence=country_of_residence, phone_number=phone_number
        )  # agency_id=agency_id, program_id=program_id
        db.session.add(new_advisor)
        db.session.commit()
        flash("Advisor registration successful. Please login.", "success")
        return redirect(url_for('login_advisor'))
    # GET: Retrieve lists of agencies and programs
    # agencies = Agency.query.all()
    # programs = Program.query.all()
    # , agencies=agencies, programs=programs
    return render_template('register_advisor.html', form=form)


@app.route('/login/advisor', methods=['GET', 'POST'])
def login_advisor():
    form = AdvisorLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        advisor = Advisor.query.filter_by(email=email).first()
        if advisor and check_password_hash(advisor.password, password):
            session['advisor'] = advisor.id
            flash("Logged in successfully", "success")
            return redirect(url_for('advisor_dashboard', advisor_id=advisor.id))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for('login_advisor'))
    return render_template('login_advisor.html', form=form)


@app.route('/advisors/<advisor_id>/dashboard')
def advisor_dashboard(advisor_id):
    if session.get('advisor') != advisor_id:
        flash("Please login as advisor", "warning")
        return redirect(url_for('login_advisor'))
    advisor = Advisor.query.get_or_404(advisor_id)
    programs = Program.query.filter_by(agency_id=advisor.agency_id).all()
    return render_template('advisor_dashboard.html', advisor=advisor, programs=programs)


@app.route('/advisors/<advisor_id>/dashboard/students')
def advisor_students(advisor_id):
    if session.get('advisor') != advisor_id:
        flash("Please login as advisor", "warning")
        return redirect(url_for('login_advisor'))
    return render_template('advisor_students.html')


@app.route('/advisors/<advisor_id>/profile', methods=['GET', 'POST'])
def advisor_profile(advisor_id):
    if session.get('advisor') != advisor_id:
        flash("Please login as advisor", "warning")
        return redirect(url_for('login_advisor'))
    advisor = Advisor.query.get_or_404(advisor_id)
    if request.method == 'POST':
        advisor.full_name = request.form.get('full_name')
        db.session.commit()
        flash("Profile updated", "success")
        return redirect(url_for('advisor_profile', advisor_id=advisor_id))
    return render_template('advisor_profile.html', advisor=advisor)

@app.route('/advisors/<string:advisor_id>/choose_program', methods=['POST'])
def choose_program(advisor_id):
    # Get the selected program from the form submission
    program_id = request.form.get('program_id')
    advisor = Advisor.query.get_or_404(advisor_id)
    
    # Update the advisor's chosen program
    advisor.program_id = program_id
    db.session.commit()
    
    flash("Program selected successfully", "success")
    return redirect(url_for('advisor_dashboard', advisor_id=advisor_id))

@app.route('/assign_student/<string:advisor_id>', methods=['POST'])
def assign_student(advisor_id):
    student_id = request.form.get('student_id')
    if not student_id:
        flash("No student selected", "warning")
        advisor = Advisor.query.get_or_404(advisor_id)
        return redirect(url_for('agency_advisors', agency_id=advisor.agency_id))
    # Check if the student is already assigned (you may adjust this logic as needed)
    existing_assignment = AdvisorAssignment.query.filter_by(student_id=student_id).first()
    if existing_assignment:
        flash("This student is already assigned", "warning")
    else:
        new_assignment = AdvisorAssignment(id=generate_uuid(), advisor_id=advisor_id, student_id=student_id)
        db.session.add(new_assignment)
        db.session.commit()
        flash("Student assigned successfully", "success")
    advisor = Advisor.query.get_or_404(advisor_id)
    return redirect(url_for('agency_advisors', agency_id=advisor.agency_id))

@app.route('/advisors/<string:advisor_id>/delete', methods=['POST'])
def delete_advisor_assignment(advisor_id):
    advisor = Advisor.query.get_or_404(advisor_id)
    advisor.program_id = None  # Reset the advisor's application
    # Optionally, you may also delete any student assignments associated with this advisor.
    db.session.commit()
    flash("Advisor application deleted", "success")
    return redirect(url_for('agency_advisors', agency_id=advisor.agency_id))


@app.route('/error')
def error():
    error_message = request.args.get(
        'msg', "An error occurred. Please try again.")
    return render_template('error.html', error_message=error_message)


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
