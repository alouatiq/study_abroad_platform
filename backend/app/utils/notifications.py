from datetime import datetime, timedelta
from app.models.application import Application
from app.utils.email import send_email

def check_application_deadlines():
    """Check for upcoming application deadlines and send notifications"""
    # Get applications with deadlines within the next 7 days
    upcoming_deadline = datetime.now() + timedelta(days=7)
    applications = Application.query.filter(
        Application.deadline <= upcoming_deadline,
        Application.status == 'pending'
    ).all()
    
    for application in applications:
        days_remaining = (application.deadline - datetime.now()).days
        
        # Send email to student
        send_email(
            to_email=application.student.email,
            subject=f"Deadline Reminder: {application.program.name}",
            body=f"""
            Dear {application.student.name},
            
            This is a reminder that your application for {application.program.name} 
            at {application.program.university} is due in {days_remaining} days.
            
            Please ensure all required documents are submitted before the deadline.
            
            Best regards,
            Study Abroad Platform Team
            """
        )
        
        # Send email to advisor if assigned
        if application.advisor:
            send_email(
                to_email=application.advisor.email,
                subject=f"Student Application Deadline: {application.student.name}",
                body=f"""
                Dear Advisor,
                
                The application for {application.student.name} to {application.program.name} 
                is due in {days_remaining} days.
                
                Please review their progress and provide any necessary assistance.
                
                Best regards,
                Study Abroad Platform Team
                """
            )

def notify_document_upload(document):
    """Send notification when a new document is uploaded"""
    application = document.application
    
    # Notify student
    send_email(
        to_email=application.student.email,
        subject=f"Document Upload Confirmation: {document.name}",
        body=f"""
        Dear {application.student.name},
        
        Your document "{document.name}" has been successfully uploaded for your
        {application.program.name} application.
        
        Our team will review it shortly.
        
        Best regards,
        Study Abroad Platform Team
        """
    )
    
    # Notify advisor if assigned
    if application.advisor:
        send_email(
            to_email=application.advisor.email,
            subject=f"New Document Upload: {application.student.name}",
            body=f"""
            Dear Advisor,
            
            {application.student.name} has uploaded a new document ({document.name})
            for their {application.program.name} application.
            
            Please review it at your earliest convenience.
            
            Best regards,
            Study Abroad Platform Team
            """
        )
