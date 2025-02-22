$(document).ready(function() {
    // Load initial programs
    loadPrograms();

    // Handle search form submission
    $('#searchForm').submit(function(e) {
        e.preventDefault();
        const searchData = {
            budget_min: $('#budgetMin').val(),
            budget_max: $('#budgetMax').val(),
            destination: $('#destination').val(),
            field_of_study: $('#fieldOfStudy').val()
        };
        loadPrograms(searchData);
    });

    // Handle questionnaire form submission
    $('#findMatchingPrograms').click(function() {
        const formData = new FormData($('#questionnaireForm')[0]);
        const searchData = {
            budget_min: formData.get('budgetMin'),
            budget_max: formData.get('budgetMax'),
            destination: Array.from(formData.getAll('destinations')).join(','),
            language: formData.get('language'),
            field_of_study: formData.get('fieldOfStudy')
        };
        loadPrograms(searchData);
        $('#questionnaireModal').modal('hide');
    });

    function loadPrograms(searchData = {}) {
        $.ajax({
            url: `${config.API_URL}/api/programs/search`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(searchData),
            success: function(programs) {
                displayPrograms(programs);
            },
            error: function(xhr, status, error) {
                console.error('Error loading programs:', error);
                const errorMsg = xhr.responseJSON?.error || 'Failed to load programs. Please try again.';
                alert(errorMsg);
            }
        });
    }

    function displayPrograms(programs) {
        const programList = $('#programList');
        programList.empty();

        if (programs.length === 0) {
            programList.html('<div class="col-12"><div class="alert alert-info">No programs found matching your criteria.</div></div>');
            return;
        }

        programs.forEach(program => {
            const programCard = `
                <div class="col-md-6 col-lg-4">
                    <div class="card program-card h-100">
                        <div class="card-body">
                            <h5 class="card-title">${program.name}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">${program.university}</h6>
                            <p class="card-text">
                                <strong>Location:</strong> ${program.country}<br>
                                <strong>Field:</strong> ${program.field_of_study}<br>
                                <strong>Duration:</strong> ${program.duration_months} months<br>
                                <strong>Tuition:</strong> €${program.tuition_fee.toLocaleString()}
                            </p>
                        </div>
                        <div class="card-footer bg-transparent border-top-0">
                            <a href="#" class="btn btn-primary w-100" 
                               onclick="viewProgramDetails(${program.id})">View Details</a>
                        </div>
                    </div>
                </div>
            `;
            programList.append(programCard);
        });
    }
});

function viewProgramDetails(programId) {
    $.ajax({
        url: `${config.API_URL}/api/programs/${programId}`,
        method: 'GET',
        success: function(program) {
            const detailsHtml = `
                <div class="program-details">
                    <h4>${program.name}</h4>
                    <h5 class="text-muted">${program.university}</h5>
                    
                    <div class="mt-4">
                        <h6>Program Overview</h6>
                        <p>${program.description}</p>
                    </div>
                    
                    <div class="mt-4">
                        <h6>Key Details</h6>
                        <ul class="list-unstyled">
                            <li><strong>Location:</strong> ${program.country}</li>
                            <li><strong>Duration:</strong> ${program.duration_months} months</li>
                            <li><strong>Tuition Fee:</strong> €${program.tuition_fee.toLocaleString()}</li>
                            <li><strong>Language Requirement:</strong> ${program.language_requirement}</li>
                        </ul>
                    </div>
                    
                    <div class="mt-4">
                        <h6>Eligibility Criteria</h6>
                        <p>${program.eligibility_criteria}</p>
                    </div>
                    
                    <div class="mt-4">
                        <h6>Available Scholarships</h6>
                        <p>${program.available_scholarships}</p>
                    </div>
                </div>
            `;
            
            $('#programDetailsContent').html(detailsHtml);
            $('#programDetailsModal').modal('show');
        },
        error: function(xhr, status, error) {
            console.error('Error loading program details:', error);
            alert('Failed to load program details. Please try again.');
        }
    });
}

// Handle Apply Now button click
$('#applyNow').click(function() {
    $('#programDetailsModal').modal('hide');
    $('#applicationModal').modal('show');
});

// Handle application form submission
$('#submitApplication').click(function() {
    const form = $('#applicationForm')[0];
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const applicationData = {
        email: $('#studentEmail').val(),
        name: $('#studentName').val(),
        phone: $('#phoneNumber').val(),
        start_date: $('#startDate').val(),
        comments: $('#comments').val()
    };

    // For MVP, just show success message and redirect to dashboard
    alert('Application submitted successfully! You will be redirected to your dashboard.');
    window.location.href = 'dashboard.html';
});
