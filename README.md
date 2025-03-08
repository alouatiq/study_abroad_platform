# Study Abroad Platform

## Overview

The Study Abroad Platform is a web application designed to simplify the process of studying abroad for students. It allows students to explore programs, connect with study abroad agencies and student advisors, and track their application progress. Agencies can manage programs, assign advisors, and offer additional services, ensuring a seamless experience for students.

## Features

- Student Registration and Login
- Program Discovery with Filtering
- Agency Registration and Management
- Student-Advisor Assignment
- Search and Filter for Programs
- Dashboard for Students, Agencies, and Advisors

## Tech Stack

- Frontend: HTML, CSS, JavaScript, Bootstrap
- Backend: Flask (Python), SQLAlchemy
- Database: MySQL

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/study-abroad-platform.git
   cd study-abroad-platform
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. login to MySQL database as root:

mysql -u root -p

5. # Create the database and its user with previleges Inside the MySQL shell

CREATE DATABASE IF NOT EXISTS study_abroad_platform;

CREATE USER IF NOT EXISTS 'portfolio_dev' @'localhost' IDENTIFIED BY 'portfolio_dev_pwd';

GRANT ALL PRIVILEGES ON `study_abroad_platform`.\* TO 'portfolio_dev' @'localhost';

GRANT
SELECT
ON `performance_schema`.\* TO 'portfolio_dev' @'localhost';

FLUSH PRIVILEGES;
EXIT

6. # Set up the database migration:

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

7. # Run the application:
   ```bash
   flask run
   ```

## Usage

- Visit `http://127.0.0.1:5000/` in your web browser to access the Study Abroad Platform.
- Register as a student, agency, or advisor to explore the features.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
