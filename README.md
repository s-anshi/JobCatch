# JobCatch: Your AI-Powered Career Companion

**JobCatch** is a streamlined Flask web application designed to help job seekers instantly evaluate their resumes against 25 different job roles. It provides predictive analytics, resume scoring, skill extraction, and tailored interview preparation — all powered by a transparent, rule-based matching engine.

---

## 🚀 Features

- **Resume Upload & Parsing**: Supports PDF and DOCX formats.
- **Smart Role Prediction**: Automatically detects the best job role out of 25 categories based on your resume content.
- **Resume Score**: Gives your resume a score (0-100) based on structural checks (contact info, sections, length).
- **Skill Gap Analysis**: Extracts technical skills found in your resume and highlights exactly what you are missing for your target role.
- **Suggested Skills**: Recommends trending skills to learn for career growth.
- **User Dashboard**: Tracks your upload history, average score, and recent predictions.
- **Interview Prep**: Provides a curated list of interview questions and answers for each of the 25 job roles.
- **Secure Authentication**: Simple, secure email and password login system with password hashing.

---

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Werkzeug
- **Database**: MySQL (via `mysql-connector-python`)
- **Document Parsing**: PyPDF2 (for PDFs), python-docx (for Word documents)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript, Jinja2 Templates, FontAwesome Icons
- **ML Layer**: Pure Python keyword matching engine (no opaque models, 100% explainable)

---

## ⚙️ Local Development Setup

### 1. Prerequisites
- Python 3.9+
- MySQL Server running locally

### 2. Database Setup
Create a new MySQL database and a dedicated user for the application:
```bash
sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS jobcatch_db; CREATE USER 'jobcatch_user'@'localhost' IDENTIFIED BY 'jobcatch_password'; GRANT ALL PRIVILEGES ON jobcatch_db.* TO 'jobcatch_user'@'localhost'; FLUSH PRIVILEGES;"
```

### 3. Installation
Clone the repository and install dependencies inside a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root directory:
```env
SECRET_KEY=my-super-secret-key-123

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=jobcatch_user
MYSQL_PASSWORD=jobcatch_password
MYSQL_DATABASE=jobcatch_db
```

### 5. Run the Application
Start the Flask development server:
```bash
python run.py
```
The application will automatically create the required database tables (`users`, `resume_uploads`) on first run.

Visit `http://127.0.0.1:5000` in your browser.

---

## 📁 Project Structure

```
JobCatch/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Environment configuration
│   ├── models.py            # MySQL database layer
│   ├── auth/                # Login, Register
│   ├── main/                # Home, Dashboard
│   ├── resume/              # Upload, History, Interview Prep
│   └── ml/
│       ├── predict.py       # Resume analysis engine
│       └── data.py          # Role keywords and interview Q&A
├── static/
│   ├── css/style.css        # Unified stylesheet
│   └── js/main.js           # Shared JavaScript
├── templates/               # Jinja2 HTML templates
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 👤 Developer
**Sudhanshi Patidar**
