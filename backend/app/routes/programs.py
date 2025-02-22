from flask import Blueprint, request, jsonify
from app.models.program import Program
from app import db

bp = Blueprint('programs', __name__, url_prefix='/api/programs')

@bp.route('/search', methods=['POST'])
def search_programs():
    data = request.get_json()
    
    # Extract search criteria with defaults
    budget_min = float(data.get('budget_min', 0))
    budget_max = float(data.get('budget_max', float('inf')))
    destination = data.get('destination')
    language = data.get('language')
    field_of_study = data.get('field_of_study')
    
    # Build query with flexible matching
    query = Program.query
    
    # Budget range (inclusive)
    if budget_min >= 0 and budget_max > budget_min:
        query = query.filter(Program.tuition_fee.between(budget_min, budget_max))
    
    # Destination (case-insensitive)
    if destination:
        query = query.filter(db.func.lower(Program.country).like(f'%{destination.lower()}%'))
    
    # Language requirement (partial match)
    if language:
        query = query.filter(db.func.lower(Program.language_requirement).like(f'%{language.lower()}%'))
    
    # Field of study (partial match)
    if field_of_study:
        query = query.filter(db.func.lower(Program.field_of_study).like(f'%{field_of_study.lower()}%'))
    
    programs = query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'university': p.university,
        'country': p.country,
        'field_of_study': p.field_of_study,
        'tuition_fee': p.tuition_fee,
        'duration_months': p.duration_months,
        'language_requirement': p.language_requirement
    } for p in programs])

@bp.route('/<int:program_id>', methods=['GET'])
def get_program(program_id):
    program = Program.query.get_or_404(program_id)
    return jsonify({
        'id': program.id,
        'name': program.name,
        'university': program.university,
        'country': program.country,
        'field_of_study': program.field_of_study,
        'tuition_fee': program.tuition_fee,
        'duration_months': program.duration_months,
        'language_requirement': program.language_requirement,
        'description': program.description,
        'eligibility_criteria': program.eligibility_criteria,
        'available_scholarships': program.available_scholarships
    })
