from models import Student, Agency, Program, Advisor, StudentProgram, AdvisorAssignment, AdvisorApplication
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from config import Config
from datetime import datetime
import uuid
import os
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


@app.route('/')
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
        query = query.filter(
            Advisor.country_of_residence.ilike(f'%{country}%'))
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
        assignments = AdvisorAssignment.query.filter_by(
            advisor_id=advisor.id).all()
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


@app.route('/programs/<program_id>', methods=['GET', 'POST'])
def program_detail(program_id):
    program = Program.query.get_or_404(program_id)
    agency = Agency.query.filter_by(id=program.agency_id).first()
    return render_template('program_detail.html', program=program, agency=agency)


@app.route('/register/student/<program_id>', methods=['GET', 'POST'])
def register_student(program_id=0):
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        full_name = form.full_name.data
        password = generate_password_hash(form.password.data)
        country_of_residence = form.country_of_residence.data
        nationality = form.nationality.data
        phone_number = form.phone_number.data

        if Student.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for('register_student', program_id=program_id))

        new_student = Student(
            id=generate_uuid(),
            email=email,
            full_name=full_name,
            password=password, phone_number=phone_number, nationality=nationality,
            country_of_residence=country_of_residence
        )
        db.session.add(new_student)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        if program_id != "0":
            # print("apply_to_program")
            return redirect(url_for('login_student', program_id=program_id))
        else:
            return redirect(url_for('login_student', program_id=0))
    else:
        for err in form.confirm_password.errors:
            flash(err, 'danger')
        for err in form.email.errors:
            flash(err, 'danger')
        for err in form.full_name.errors:
            flash(err, 'danger')
    return render_template('register_student.html', form=form, program_id=program_id)


@app.route('/login/student/<program_id>', methods=['GET', 'POST'])
def login_student(program_id=0):
    form = StudentLoginForm()
    # print(f"0- program_id = {program_id}")

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        student = Student.query.filter_by(email=email).first()
        # print(f"program_id = {program_id}")
        if student and check_password_hash(student.password, password):
            session['student'] = student.id
            flash("Logged in successfully", "success")
            if program_id != "0":
                return redirect(url_for('program_detail', program_id=program_id))
            else:
                return redirect(url_for('student_dashboard', student_id=student.id))
        else:

            flash("Invalid credentials", "danger")
    else:
        for err in form.email.errors:
            flash(err, 'danger')
    return render_template('login_student.html', form=form, program_id=program_id)


@app.route('/students/<student_id>/dashboard')
def student_dashboard(student_id):
    if not is_logged_in('student', student_id):
        flash("You need to be logged in as a student", "warning")
        return redirect(url_for('login_student', program_id=0))
    student = Student.query.get_or_404(student_id)
    applications = StudentProgram.query.filter_by(student_id=student_id).all()
    return render_template('student_dashboard.html', student=student, applications=applications)


@app.route('/students/<student_id>/apply/<program_id>', methods=['POST'])
def apply_to_program(student_id, program_id):
    if not is_logged_in('student', student_id):
        flash("You need to be logged in to apply", "warning")
        return redirect(url_for('register_student', program_id=program_id))

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
        return redirect(url_for('login_student', program_id=0))

    student_folder = os.path.join('static', 'documents', student_id)
    os.makedirs(student_folder, exist_ok=True)

    if request.method == 'POST':
        for file_key in ['picture', 'id_document', 'certificate']:
            if file_key in request.files:
                file = request.files[file_key]
                if file:
                    file_path = os.path.join(student_folder, file.filename)
                    file.save(file_path)

        flash("Documents updated", "success")
        return redirect(url_for('student_documents', student_id=student_id))

    documents = []
    for filename in os.listdir(student_folder):
        documents.append(filename)

    return render_template('student_documents.html', documents=documents, student_id=student_id)


@app.route('/students/<student_id>/dashboard/documents/delete/<document>', methods=['POST'])
def delete_document(student_id, document):
    if not is_logged_in('student', student_id):
        flash("Please login to delete your documents", "warning")
        return redirect(url_for('login_student', program_id=0))

    student_folder = os.path.join('static', 'documents', student_id)
    file_path = os.path.join(student_folder, document)

    if os.path.exists(file_path):
        os.remove(file_path)
        flash("Document deleted", "success")
    else:
        flash("Document not found", "danger")

    return redirect(url_for('student_documents', student_id=student_id))


@app.route('/students/<student_id>/profile', methods=['GET', 'POST'])
def student_profile(student_id):
    if not is_logged_in('student', student_id):
        flash("Please login to access your profile", "warning")
        return redirect(url_for('login_student', program_id=0))
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.full_name = request.form.get('full_name')
        student.phone_number = request.form.get('phone_number')
        student.nationality = request.form.get('nationality')
        student.country_of_residence = request.form.get('country_of_residence')
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

    print(f"program_id ={program_id}")
    # Delete the Program id in the advisor_application table
    advisors_applis = AdvisorApplication.query.filter_by(
        program_id=program_id).all()

    [db.session.delete(item) for item in advisors_applis]
    # Delete the Program id in the  advisor_assignments table
    assignments = AdvisorAssignment.query.filter_by(program_id=program_id)
    [db.session.delete(item) for item in assignments]
    # Delete the Program id in the student_programs table
    students_applis = StudentProgram.query.filter_by(program_id=program_id)
    [db.session.delete(item) for item in students_applis]

    # Delete the Programe from program tables
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
        description = form.description.data
        website = form.website.data

        if Agency.query.filter_by(name=name).first():
            flash("Agency already exists", "danger")
            return redirect(url_for('register_agency'))

        new_agency = Agency(
            id=generate_uuid(),
            name=name,
            password=password, description=description, website=website
        )
        db.session.add(new_agency)
        db.session.commit()
        flash("Agency registration successful. Please login.", "success")
        return redirect(url_for('login_agency'))
    else:
        for err in form.confirm_password.errors:
            flash(err, 'danger')
        for err in form.website.errors:
            flash(err, 'danger')
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

    return render_template(
        'agency_dashboard.html', agency=agency, programs=programs)


@app.route('/agencies/<agency_id>/dashboard/students')
def agency_students(agency_id):
    if session.get('agency') != agency_id:
        flash("Please login as agency", "warning")
        return redirect(url_for('login_agency'))

    # Fetch all programs offered by the agency
    programs = Program.query.filter_by(agency_id=agency_id).all()

    # Fetch all student applications for these programs
    student_applications = StudentProgram.query.join(
        Program, StudentProgram.program_id == Program.id).filter(Program.agency_id == agency_id).all()

    # Fetch all advisors who have offered assistance to these programs
    advisor_applications = AdvisorApplication.query.join(Program, AdvisorApplication.program_id == Program.id).filter(
        Program.agency_id == agency_id, AdvisorApplication.assistance_approval == True).all()

    # Get approved advisor for certain program to assist certain student
    assigned_advisors = AdvisorAssignment.query.join(
        Advisor, AdvisorAssignment.advisor_id == Advisor.id).all()

    return render_template('agency_students.html', agency_id=agency_id, programs=programs,
                           student_applications=student_applications,
                           advisors=advisor_applications,
                           assigned_advisors=assigned_advisors)


@app.route('/agencies/<agency_id>/dashboard/students/update_status/<application_id>', methods=['POST'])
def update_application_status(agency_id, application_id):
    if session.get('agency') != agency_id:
        flash("Please login as agency", "warning")
        return redirect(url_for('login_agency'))

    application = StudentProgram.query.get_or_404(application_id)
    new_status = request.form.get('status')
    application.status = new_status
    db.session.commit()
    flash("Application status updated successfully", "success")
    return redirect(url_for('agency_students', agency_id=agency_id))


@app.route('/agencies/<agency_id>/dashboard/students/assign_advisor/<application_id>', methods=['POST'])
def assign_advisor_to_student(agency_id, application_id):
    if session.get('agency') != agency_id:
        flash("Please login as agency", "warning")
        return redirect(url_for('login_agency'))

    application = StudentProgram.query.get_or_404(application_id)
    advisor_id = request.form.get('advisor_id')
    if not advisor_id:
        flash("No advisor selected", "danger")
        return redirect(url_for('agency_students', agency_id=agency_id))

    existing_assignment = AdvisorAssignment.query.filter_by(
        student_id=application.student_id, program_id=application.program_id).first()

    if existing_assignment:
        flash("The assigned advisor has changed!", "warning")
        existing_assignment.advisor_id = advisor_id
        db.session.commit()
        return redirect(url_for('agency_students', agency_id=agency_id))

    new_assignment = AdvisorAssignment(
        id=generate_uuid(),
        advisor_id=advisor_id,
        student_id=application.student_id,
        program_id=application.program_id
    )
    db.session.add(new_assignment)
    db.session.commit()
    flash("A new advisor is assigned successfully", "success")
    return redirect(url_for('agency_students', agency_id=agency_id))


@app.route('/agencies/<string:agency_id>/dashboard/advisors', methods=['GET', 'POST'])
def agency_advisors(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    my_programs = Program.query.filter_by(agency_id=agency_id).all()

    # advisor_applications = [advisors_program0, advisors_program1,....]
    advisor_applications = [AdvisorApplication.query.filter_by(
        program_id=prog.id).all() for prog in my_programs]

    advisors_list = []

    for agency_programs in advisor_applications:
        for appli in agency_programs:
            advisor_proposal = {}

            # # construct advisor_proposal
            advisor_proposal['id'] = appli.id
            advisor_proposal['name'] = Advisor.query.filter_by(
                id=appli.advisor_id).all()[0].full_name
            print(f"advisor_proposal['name'] = {advisor_proposal['name']}")
            advisor_proposal['country of residence'] = Advisor.query.filter_by(
                id=appli.advisor_id).all()[0].country_of_residence
            print(
                f"advisor_proposal['country of residence'] = {advisor_proposal['country of residence']}")
            advisor_proposal['program name'] = Program.query.filter_by(
                id=appli.program_id).all()[0].name
            print(
                f"advisor_proposal['program name'] = {advisor_proposal['program name']}")
            advisor_proposal['university'] = Program.query.filter_by(
                id=appli.program_id).all()[0].university
            print(
                f"advisor_proposal['university'] = {advisor_proposal['university']}")
            advisor_proposal['assistance status'] = "Approved" if appli.assistance_approval else "Rejected"
            print(
                f"advisor_proposal['assistance status'] = {advisor_proposal['assistance status']}")
            # append in advisors_list
            advisors_list.append(advisor_proposal)
            print(f"--------------------------------------------")
            print()
    print(f"advisors_list = {advisors_list}")
    print(f"--------------------------------------------")
    if request.method == 'POST':
        if session.get('agency') != agency_id:
            flash("Please login as agency", "warning")
            return redirect(url_for('login_agency'))

        appli_id = request.form["appli_id"]
        assistance_approval = request.form["assistance_approval"]

        appli = AdvisorApplication.query.filter_by(id=appli_id,).first()
        appli.assistance_approval = int(assistance_approval)
        print(f"appli = {appli}")
        print(f"appli.id = {appli.id}")

        db.session.commit()
        flash("Advisor application is successfully modified!", "success")
        return redirect(url_for('agency_advisors', agency_id=agency_id))

    return render_template('agency_advisors.html', advisors_list=advisors_list, agency_id=agency_id)


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
    # Check if the student is already assigned
    existing_assignment = AdvisorAssignment.query.filter_by(
        student_id=student_id).first()
    if existing_assignment:
        flash("This student is already assigned to an advisor.", "warning")
        return redirect(url_for('agency_advisors', agency_id=agency_id))
    new_assignment = AdvisorAssignment(
        id=generate_uuid(),
        advisor_id=advisor_id,
        student_id=student_id
    )
    db.session.add(new_assignment)
    db.session.commit()
    flash("Student assigned successfully", "success")
    return redirect(url_for('agency_advisors', agency_id=agency_id))


@app.route('/agencies/<agency_id>/profile', methods=['GET', 'POST'])
def agency_profile(agency_id):
    if session.get('agency') != agency_id:
        flash("Please login as agency", "warning")
        return redirect(url_for('login_agency'))
    agency = Agency.query.get_or_404(agency_id)
    if request.method == 'POST':
        agency.website = request.form.get('website')
        agency.description = request.form.get('description')
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

        try:
            available_scholarships = bool(int(available_scholarships))
        except:
            available_scholarships = False

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


@app.route('/register/advisor/<program_id>', methods=['GET', 'POST'])
def register_advisor(program_id=0):
    form = AdvisorRegistrationForm()
    # Populate the agency choices from the database
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        country_of_residence = form.country_of_residence.data
        phone_number = form.phone_number.data

        if Advisor.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for('register_advisor', program_id=program_id))

        new_advisor = Advisor(
            id=generate_uuid(),
            full_name=full_name,
            email=email,
            password=password,
            country_of_residence=country_of_residence,
            phone_number=phone_number
        )
        db.session.add(new_advisor)
        db.session.commit()
        flash("Advisor registration successful. Please login.", "success")

        if program_id != "0":
            # print("apply_to_program")
            return redirect(url_for('login_advisor', program_id=program_id))
            # return redirect(url_for('login_student', program_id=program_id))
        else:
            return redirect(url_for('login_advisor', program_id=0))

    else:
        for err in form.confirm_password.errors:
            flash(err, 'danger')
        for err in form.email.errors:
            flash(err, 'danger')
        for err in form.full_name.errors:
            flash(err, 'danger')
    return render_template('register_advisor.html', form=form, program_id=program_id)


@app.route('/login/advisor/<program_id>', methods=['GET', 'POST'])
def login_advisor(program_id=0):
    form = AdvisorLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        advisor = Advisor.query.filter_by(email=email).first()
        if advisor and check_password_hash(advisor.password, password):
            session['advisor'] = advisor.id
            flash("Logged in successfully", "success")

            if program_id != "0":
                return redirect(url_for('program_detail', program_id=program_id))
            else:
                return redirect(url_for('advisor_dashboard', advisor_id=advisor.id))
        else:
            flash("Invalid credentials", "danger")
            # return redirect(url_for('login_advisor'))
    else:
        for err in form.email.errors:
            flash(err, 'danger')
    return render_template('login_advisor.html', form=form, program_id=program_id)


@app.route('/advisors/<string:advisor_id>/dashboard')
def advisor_dashboard(advisor_id):
    if session.get('advisor') != advisor_id:
        flash("Please login as advisor", "warning")
        return redirect(url_for('login_advisor'))
    advisor = Advisor.query.get_or_404(advisor_id)
    # available_programs = Program.query.filter_by(
    #     agency_id=advisor.agency_id).all()
    # Advisor's applications:
    applications = AdvisorApplication.query.filter_by(
        advisor_id=advisor_id).all()
    # available_programs=available_programs,
    return render_template('advisor_dashboard.html', advisor=advisor, applications=applications)


@app.route('/advisors/<advisor_id>/dashboard/students')
def advisor_students(advisor_id):
    if session.get('advisor') != advisor_id:
        flash("Please login as advisor", "warning")
        return redirect(url_for('login_advisor'))

    advisor = Advisor.query.get_or_404(advisor_id)
    return render_template('advisor_students.html', advisor=advisor)


@app.route('/advisors/<advisor_id>/profile', methods=['GET', 'POST'])
def advisor_profile(advisor_id):
    if session.get('advisor') != advisor_id:
        flash("Please login as advisor", "warning")
        return redirect(url_for('login_advisor'))
    advisor = Advisor.query.get_or_404(advisor_id)
    if request.method == 'POST':
        advisor.full_name = request.form.get('full_name')
        advisor.phone_number = request.form.get('phone_number')
        advisor.country_of_residence = request.form.get('country_of_residence')
        db.session.commit()
        flash("Profile updated", "success")
        return redirect(url_for('advisor_profile', advisor_id=advisor_id))
    return render_template('advisor_profile.html', advisor=advisor)


@app.route('/advisors/<string:advisor_id>/apply/<string:program_id>', methods=['POST'])
def offer_assistance(advisor_id, program_id):
    if session.get('advisor') != advisor_id:
        flash("Please login as advisor", "warning")
        return redirect(url_for('login_advisor'))

    # Check if an application for this program already exists:
    existing_application = AdvisorApplication.query.filter_by(
        advisor_id=advisor_id, program_id=program_id).first()
    if existing_application:
        flash("You have already applied for this program.", "warning")
    else:
        new_application = AdvisorApplication(
            id=generate_uuid(),
            advisor_id=advisor_id,
            program_id=program_id,
            created_at=datetime.utcnow()
        )
        db.session.add(new_application)
        db.session.commit()
        flash("Application submitted successfully.", "success")
    return redirect(url_for('advisor_dashboard', advisor_id=advisor_id))


@app.route('/advisors/<string:advisor_id>/delete_program', methods=['POST'])
def delete_program_application(advisor_id):
    advisor = Advisor.query.get_or_404(advisor_id)
    advisor.program_id = None  # remove the selected program
    db.session.commit()
    flash("Program selection removed.", "success")
    return redirect(url_for('advisor_dashboard', advisor_id=advisor_id))


'''
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
'''


@app.route('/advisor_applications/<string:application_id>/delete', methods=['POST'])
def delete_advisor_application(application_id):
    application = AdvisorApplication.query.get_or_404(application_id)
    advisor_id = application.advisor_id
    db.session.delete(application)
    db.session.commit()
    flash("Application deleted successfully", "success")
    return redirect(url_for('advisor_dashboard', advisor_id=advisor_id))


# @app.route('/programs/<string:program_id>/offer_assistance')
# def offer_assistance(program_id):
#     # Ensure the advisor remains logged in (session check) if needed.
#     program = Program.query.get_or_404(program_id)
#     # Render a dedicated page or modal to offer assistance.
#     return render_template('offer_assistance.html', program=program)


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
