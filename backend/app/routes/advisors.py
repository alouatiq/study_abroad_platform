from flask import Blueprint, request, jsonify
from app.models.application import Application
from app.models.user import User
from app import db

bp = Blueprint('advisors', __name__, url_prefix='/api/advisors')

@bp.route('/applications', methods=['GET'])
def get_advisor_applications():
    advisor_id = request.args.get('advisor_id')
    status_filter = request.args.get('status')
    
    query = Application.query.filter_by(advisor_id=advisor_id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    applications = query.all()
    
    return jsonify([{
        'id': app.id,
        'student': {
            'id': app.student.id,
            'email': app.student.email
        },
        'program': {
            'id': app.program.id,
            'name': app.program.name,
            'university': app.program.university,
            'country': app.program.country
        },
        'status': app.status,
        'submitted_at': app.submitted_at,
        'documents': [{
            'id': doc.id,
            'name': doc.name,
            'uploaded_at': doc.uploaded_at
        } for doc in app.documents],
        'messages_count': len(app.messages)
    } for app in applications])

@bp.route('/applications/<int:application_id>/status', methods=['PUT'])
def update_application_status():
    data = request.get_json()
    application = Application.query.get_or_404(data['application_id'])
    application.status = data['status']
    db.session.commit()
    return jsonify({'status': application.status})
