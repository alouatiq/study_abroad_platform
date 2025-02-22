from flask import Blueprint, request, jsonify
from app.models.application import Application
from app.models.user import User
from app import db

bp = Blueprint('agents', __name__, url_prefix='/api/agents')

@bp.route('/applications', methods=['GET'])
def get_agent_applications():
    agent_id = request.args.get('agent_id')
    status_filter = request.args.get('status')
    
    query = Application.query.filter_by(agent_id=agent_id)
    
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
        'last_activity': max([msg.created_at for msg in app.messages] + [doc.uploaded_at for doc in app.documents] + [app.submitted_at]) if app.messages or app.documents else app.submitted_at,
        'documents_count': len(app.documents),
        'messages_count': len(app.messages),
        'engagement_score': len(app.messages) + len(app.documents)  # Simple engagement metric
    } for app in applications])

@bp.route('/assignments', methods=['POST'])
def assign_application():
    data = request.get_json()
    application = Application.query.get_or_404(data['application_id'])
    application.agent_id = data['agent_id']
    db.session.commit()
    return jsonify({'success': True})
