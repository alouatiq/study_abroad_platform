from flask import Blueprint, request, jsonify
from app.models.application import Application, Document, Message
from app.utils.notifications import notify_document_upload
from app import db
from datetime import datetime

bp = Blueprint('applications', __name__, url_prefix='/api/applications')

@bp.route('', methods=['POST'])
def create_application():
    data = request.get_json()
    
    if not data or 'student_id' not in data or 'program_id' not in data:
        return jsonify({'error': 'student_id and program_id are required'}), 400
    
    application = Application(
        student_id=data['student_id'],
        program_id=data['program_id'],
        status='pending'
    )
    
    db.session.add(application)
    db.session.commit()
    
    return jsonify({
        'id': application.id,
        'status': application.status,
        'student_id': application.student_id,
        'program_id': application.program_id,
        'submitted_at': application.submitted_at
    }), 201

@bp.route('/<int:application_id>/status', methods=['GET'])
def get_application_status(application_id):
    application = Application.query.get_or_404(application_id)
    return jsonify({
        'status': application.status,
        'submitted_at': application.submitted_at,
        'documents': [{
            'name': doc.name,
            'uploaded_at': doc.uploaded_at
        } for doc in application.documents]
    })

@bp.route('/<int:application_id>/documents', methods=['POST'])
def upload_document(application_id):
    """
    For MVP, we'll store document metadata only.
    In production, this would handle actual file uploads.
    """
    if 'document_name' not in request.json:
        return jsonify({'error': 'document_name is required'}), 400
        
    document = Document(
        application_id=application_id,
        name=request.json['document_name'],
        file_path=f"mock_storage/{application_id}/{request.json['document_name']}",
        uploaded_at=datetime.utcnow()
    )
    
    db.session.add(document)
    db.session.commit()
    
    # Send notifications
    notify_document_upload(document)
    
    return jsonify({
        'id': document.id,
        'name': document.name,
        'uploaded_at': document.uploaded_at
    }), 201

@bp.route('/<int:application_id>/messages', methods=['GET', 'POST'])
def handle_messages(application_id):
    if request.method == 'GET':
        messages = Message.query.filter_by(application_id=application_id).order_by(Message.created_at.desc()).all()
        return jsonify([{
            'id': msg.id,
            'sender_id': msg.sender_id,
            'content': msg.content,
            'created_at': msg.created_at
        } for msg in messages])
    
    data = request.get_json()
    if not data or 'sender_id' not in data or 'content' not in data:
        return jsonify({'error': 'sender_id and content are required'}), 400
    
    message = Message(
        application_id=application_id,
        sender_id=data['sender_id'],
        content=data['content']
    )
    db.session.add(message)
    db.session.commit()
    
    # Notify the other party about new message
    application = Application.query.get(application_id)
    if data['sender_id'] == application.student_id:
        recipient = application.advisor if application.advisor_id else application.agent
    else:
        recipient = application.student
        
    if recipient:
        from app.utils.email import send_deadline_reminder
        send_deadline_reminder(recipient.email, application)
    
    return jsonify({
        'id': message.id,
        'sender_id': message.sender_id,
        'content': message.content,
        'created_at': message.created_at
    }), 201
