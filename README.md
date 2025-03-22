# Study Abroad Platform

## Overview

The Study Abroad Platform is a full-stack web application designed to assist students in finding the right academic programs abroad. It facilitates easy discovery of programs, agency management, student-advisor interactions, and application tracking. Agencies can manage their programs and advisors, offering end-to-end support for students.

## Key Features

- User Registration (Students, Agencies, Advisors)
- Program Catalog with Search & Filter Options
- Agency Dashboard (Program & Service Management)
- Student-Advisor Matching System
- Application Tracking (Student-Advisor-Agency workflows)
- Multi-role Dashboard (Students, Advisors, Agencies)
- Secure Login & Role-based Access Control
- Responsive UI (Bootstrap powered)

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Flask (Python) with SQLAlchemy ORM
- **Database:** MySQL
- **Migrations:** Flask-Migrate (Alembic)
- **Session Management:** Flask-Session (filesystem)

## Installation Guide

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/study-abroad-platform.git
cd study-abroad-platform
```

### 2. Setup virtual environment

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

You can either manually create the database or use the automated setup script.

#### Option 1: Manually (MySQL shell)

```bash
mysql -u root -p
```
Inside the MySQL shell:

```sql
SOURCE database_setup.sql;
```

#### Option 2: Automated Setup

To automatically create the database without entering the MySQL shell, run:

```bash
python setup_db.py
```

> This requires proper permissions and `sqlalchemy-utils` installed.

### 5. Run database migrations

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### 6. Run the application

```bash
flask run
```

Visit `http://127.0.0.1:5000/` in your browser.

## Usage Guide

- Students can browse programs, apply, and connect with advisors.
- Agencies can register programs and assign advisors.
- Advisors can manage student applications and assist them through the process.

## Screenshots

![Student Dashboard](link-to-image1)
![Program Listing](link-to-image2)
![Agency Dashboard](link-to-image3)

## Contribution Guidelines

We welcome contributions! To contribute:

1. Fork this repository.
2. Create your feature branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m 'Add Your Feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a Pull Request.

## License

This project is licensed under the MIT License.