$(document).ready(function() {
    // Mock user data (replace with actual authentication)
    const currentUser = {
        id: 1,
        email: 'student@example.com',
        role: 'student'
    };
    
    // Display user email
    $('#userEmail').text(currentUser.email);
    
    // Load initial data
    loadApplications();
    loadDocuments();
    loadMessages();
    
    // Handle tab switching
    $('.list-group-item').click(function(e) {
        e.preventDefault();
        $('.list-group-item').removeClass('active');
        $(this).addClass('active');
        
        const target = $(this).data('target');
        $('.tab-content').addClass('d-none');
        $(`#${target}Tab`).removeClass('d-none');
    });
    
    // Handle message form submission
    $('#messageForm').submit(function(e) {
        e.preventDefault();
        const message = $(this).find('input').val();
        const applicationId = $(this).data('application-id');
        if (message.trim() && applicationId) {
            sendMessage(message, applicationId);
            $(this).find('input').val('');
        }
    });
    
    function loadApplications() {
        $.ajax({
            url: `${config.API_URL}/api/applications`,
            method: 'GET',
            headers: {
                'student_id': currentUser.id
            },
            success: function(applications) {
                displayApplications(applications);
            },
            error: function(xhr, status, error) {
                console.error('Error loading applications:', error);
            }
        });
    }
    
    function displayApplications(applications) {
        const applicationsList = $('.applications-list');
        applicationsList.empty();
        
        applications.forEach(app => {
            const card = `
                <div class="card mb-3">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h5 class="card-title">${app.program.name}</h5>
                                <h6 class="card-subtitle mb-2 text-muted">${app.program.university}</h6>
                            </div>
                            <span class="badge bg-${getStatusBadgeClass(app.status)}">${app.status}</span>
                        </div>
                        <div class="progress mt-3" style="height: 5px;">
                            <div class="progress-bar" role="progressbar" style="width: ${getProgressPercentage(app)}%"></div>
                        </div>
                        <div class="mt-3">
                            <small class="text-muted">Last updated: ${new Date(app.updated_at).toLocaleDateString()}</small>
                        </div>
                    </div>
                </div>
            `;
            applicationsList.append(card);
            
            // Load messages when application card is clicked
            card.find('.view-messages').click(function() {
                const appId = $(this).data('application-id');
                $('#messageForm').data('application-id', appId);
                loadMessages(appId);
            });
        });
    }
    
    function loadDocuments() {
        // Mock document requirements
        const documents = [
            { name: 'Passport Copy', required: true, status: 'pending' },
            { name: 'Academic Transcripts', required: true, status: 'uploaded' },
            { name: 'Language Certificate', required: true, status: 'pending' },
            { name: 'CV/Resume', required: false, status: 'not_started' }
        ];
        
        const documentList = $('.document-list');
        documentList.empty();
        
        documents.forEach(doc => {
            const card = `
                <div class="card mb-3">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h5 class="card-title">${doc.name}</h5>
                                <p class="card-text">
                                    <small class="text-muted">
                                        ${doc.required ? 'Required' : 'Optional'}
                                    </small>
                                </p>
                            </div>
                            <div>
                                ${getDocumentUploadButton(doc)}
                            </div>
                        </div>
                    </div>
                </div>
            `;
            documentList.append(card);
        });
    }
    
    function loadMessages(applicationId = null) {
        if (!applicationId) {
            console.warn('No application ID provided for messages');
            return;
        }
        $.ajax({
            url: `${config.API_URL}/api/applications/${applicationId}/messages`,
            method: 'GET',
            success: function(messages) {
                displayMessages(messages);
            },
            error: function(xhr, status, error) {
                console.error('Error loading messages:', error);
            }
        });
    }
    
    function displayMessages(messages) {
        const messageList = $('.message-list');
        messageList.empty();
        
        messages.forEach(msg => {
            const messageHtml = `
                <div class="card mb-2 ${msg.sender_id === currentUser.id ? 'ms-auto' : ''}" style="max-width: 70%;">
                    <div class="card-body py-2 px-3">
                        <p class="card-text mb-1">${msg.content}</p>
                        <small class="text-muted">${new Date(msg.created_at).toLocaleString()}</small>
                    </div>
                </div>
            `;
            messageList.append(messageHtml);
        });
        
        // Scroll to bottom
        messageList.scrollTop(messageList[0].scrollHeight);
    }
    
    function sendMessage(content, applicationId = null) {
        if (!applicationId) {
            console.warn('No application ID provided for sending message');
            return;
        }
        $.ajax({
            url: `${config.API_URL}/api/applications/${applicationId}/messages`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                sender_id: currentUser.id,
                content: content
            }),
            success: function(response) {
                loadMessages();
            },
            error: function(xhr, status, error) {
                console.error('Error sending message:', error);
                alert('Failed to send message. Please try again.');
            }
        });
    }
    
    function getStatusBadgeClass(status) {
        switch(status.toLowerCase()) {
            case 'approved': return 'success';
            case 'pending': return 'warning';
            case 'rejected': return 'danger';
            default: return 'secondary';
        }
    }
    
    function getProgressPercentage(application) {
        // Calculate progress based on completed steps
        const totalSteps = 5;
        let completedSteps = 0;
        
        if (application.documents && application.documents.length > 0) completedSteps++;
        if (application.status === 'approved') completedSteps = totalSteps;
        if (application.status === 'pending') completedSteps = Math.min(completedSteps + 2, totalSteps - 1);
        
        return (completedSteps / totalSteps) * 100;
    }
    
    function getDocumentUploadButton(document) {
        switch(document.status) {
            case 'uploaded':
                return `
                    <button class="btn btn-success btn-sm" disabled>
                        <i class="bi bi-check"></i> Uploaded
                    </button>`;
            case 'pending':
                return `
                    <button class="btn btn-warning btn-sm" disabled>
                        <i class="bi bi-clock"></i> Pending Review
                    </button>`;
            default:
                return `
                    <button class="btn btn-primary btn-sm upload-document" data-document="${document.name}">
                        <i class="bi bi-upload"></i> Upload
                    </button>`;
        }
    }
    
    // Handle document upload
    $(document).on('click', '.upload-document', function() {
        const documentName = $(this).data('document');
        // TODO: Implement actual file upload
        alert(`File upload for ${documentName} coming soon!`);
    });
    
    // Handle logout
    $('#logoutBtn').click(function() {
        // TODO: Implement actual logout
        window.location.href = 'index.html';
    });
});
