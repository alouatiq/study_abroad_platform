# 📁 Project Directory Structure
```
study_abroad_platform/  
│── backend/                 # Backend (Flask API)
│   ├── app/  
│   │   ├── __init__.py       # Initialize Flask app  
│   │   ├── config.py         # Configuration settings (DB, security, etc.)
│   │   ├── models.py         # Database models (SQLAlchemy ORM)
│   │   ├── routes/           # API routes  
│   │   │   ├── students.py   # Student-related endpoints
│   │   │   ├── agencies.py   # Agency-related endpoints  
│   │   │   ├── advisors.py   # Advisor-related endpoints  
│   │   │   ├── programs.py   # Study programs endpoints  
│   │   │   ├── auth.py       # Authentication (Future enhancement)  
│   │   ├── services/         # Business logic layer  
│   │   │   ├── student_service.py  
│   │   │   ├── agency_service.py  
│   │   │   ├── advisor_service.py  
│   │   ├── utils/            # Utility functions  
│   │   │   ├── validators.py # Data validation utilities  
│   │   │   ├── helpers.py    # Helper functions  
│   │   ├── db.py             # Database connection setup  
│   ├── migrations/           # Database migrations (Flask-Migrate)  
│   ├── tests/                # Unit tests (PyTest, Unittest)
│   │   ├── test_students.py  
│   │   ├── test_agencies.py  
│   │   ├── test_advisors.py  
│   ├── wsgi.py               # Entry point for production deployment  
│── frontend/                 # Frontend (HTML, CSS, Bootstrap)
│   ├── static/               # Static assets  
│   │   ├── css/  
│   │   ├── js/  
│   │   ├── images/  
│   ├── templates/            # HTML templates (Flask Jinja)
│   │   ├── index.html        # Home page  
│   │   ├── program_list.html # Program search results  
│   │   ├── student_dashboard.html  
│   │   ├── agency_dashboard.html  
│   │   ├── advisor_dashboard.html  
│   ├── app.py                # Frontend logic (optional Flask integration)  
│── config/                   # Deployment & Environment Configs  
│   ├── docker-compose.yml    # Docker configuration (if used)  
│   ├── gunicorn_config.py    # Gunicorn settings for production  
│── docs/                     # Documentation  
│── requirements.txt          # Python dependencies  
│── .env                      # Environment variables  
│── README.md                 # Project documentation  
│── .gitignore                # Ignore unnecessary files  
```
