# Study Abroad Platform

## Overview

The **Study Abroad Platform** is a full-stack web application designed to help students discover academic programs abroad, connect with advisors, and apply through agencies. Agencies and advisors can manage programs, guide students, and track applications from end to end.

---

## 🔑 Key Features

- 👩‍🎓 User Registration (Students, Agencies, Advisors)
- 🔍 Program Catalog with Search & Filters
- 🧑‍💼 Agency Dashboard: Manage Programs & Services
- 🤝 Student-Advisor Matching System
- 📋 Application Workflow Management
- 🔐 Role-Based Access Control & Secure Login
- 📱 Responsive Interface (Bootstrap)

---

## ⚙️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Flask (Python) + Flask-WTF + SQLAlchemy + Flask-Migrate
- **Database:** PostgreSQL (via Render)
- **Deployment:**
  - Backend API: [Render](https://study-abroad-platform.onrender.com/)
  - Landing Page: [Vercel](https://study-abroad-platform.vercel.app/)

---

## 🚀 Deployed Project

- **Project API:** [https://study-abroad-platform.onrender.com/](https://study-abroad-platform.onrender.com/)
- **Landing Page:** [https://study-abroad-platform.vercel.app/](https://study-abroad-platform.vercel.app/)

---

## 🛠️ Setup Instructions (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/alouatiq/study_abroad_platform.git
cd study_abroad_platform
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file (or export manually) with:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://username:password@host:port/dbname
```

> Replace with your local or remote PostgreSQL credentials.

### 5. Run Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the app

```bash
flask run
```

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

---

## 📸 Screenshots

![Student Dashboard](https://raw.githubusercontent.com/alouatiq/study_abroad_platform/refs/heads/main/static/images/student.webp)
![Advisor Dashboard](https://raw.githubusercontent.com/alouatiq/study_abroad_platform/refs/heads/main/static/images/advisor.webp)
![Agency Dashboard](https://raw.githubusercontent.com/alouatiq/study_abroad_platform/refs/heads/main/static/images/agency.webp)

---

## 👥 Contributors

| Username | Name |
|----------|------|
| [@alouatiq](https://github.com/alouatiq) | AL OUATIQ Hassan |
| [@HajarElMannani](https://github.com/HajarElMannani) | Hajar El Mannani |
| [@Anas2018EMI](https://github.com/Anas2018EMI) | Anas AATEF |

---

## 📜 License

This project is licensed under the MIT License.
