from datetime import datetime, timedelta
from flask import current_app

def send_email(to_email, subject, body):
    """
    For MVP, just print the email that would be sent.
    In production, this would use a proper email service.
    """
    print(f"\nEmail would be sent to: {to_email}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}\n")
    return True

def send_deadline_reminder(student_email, application):
    """Send a reminder email about application deadline"""
    subject = f"Reminder: Application Deadline Approaching"
    body = f"""
    Dear Student,
    
    This is a reminder about your application to {application.program.name}.
    Please ensure all required documents are submitted before the deadline.
    
    Application Status: {application.status}
    Program: {application.program.name}
    University: {application.program.university}
    
    Best regards,
    Study Abroad Platform Team
    """
    return send_email(student_email, subject, body)
