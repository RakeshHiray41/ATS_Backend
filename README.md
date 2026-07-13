# 🚀 HireTrack – Applicant Tracking System (ATS) Backend

A production-ready **Applicant Tracking System (ATS)** backend built using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, **JWT Authentication**, and **Supabase**.

The backend provides secure REST APIs for authentication, candidate management, recruiter management, job postings, job applications, interview scheduling, company management, dashboard analytics, and cloud file storage.

---

# ✨ Features

## 🔐 Authentication

- User Registration
- User Login
- JWT Authentication
- Password Hashing (Passlib + Bcrypt)
- Role-Based Authorization
- Protected APIs

---

## 👨‍💼 Candidate Module

- Create Candidate Profile
- Update Candidate Profile
- Upload Resume
- Upload Profile Image
- Apply for Jobs
- View Applied Jobs
- View Interviews
- Candidate Dashboard

---

## 🏢 Recruiter Module

- Recruiter Registration
- Company Profile Management
- Upload Company Logo
- Create Jobs
- Update Jobs
- Delete Jobs
- View Applicants
- Schedule Interviews
- Recruiter Dashboard

---

## 💼 Job Management

- Create Job
- Update Job
- Delete Job
- Public Job Listings
- Job Details
- Search Jobs

---

## 📄 Resume & File Management

HireTrack uses **Supabase Storage** for cloud file storage.

Features:

- Upload Candidate Resume (PDF)
- Upload Candidate Profile Image
- Upload Company Logo
- Secure Cloud Storage
- Generate Public URLs
- Resume Validation
- Image Validation

Storage Buckets:

- resumes
- profile-images
- company-logos

---

## 📅 Interview Management

- Schedule Interviews
- Update Interview Status
- Candidate Interview List
- Recruiter Interview Management

---

## 📊 Dashboard

### Candidate Dashboard

- Total Applications
- Recent Applications
- Upcoming Interviews

### Recruiter Dashboard

- Total Jobs
- Total Applicants
- Scheduled Interviews

---

# 🛠 Tech Stack

### Backend

- FastAPI
- Python 3

### Database

- PostgreSQL
- SQLAlchemy ORM
- Alembic

### Authentication

- JWT
- Passlib (Bcrypt)

### Cloud Services

- Supabase Database
- Supabase Storage

### Email

- FastAPI Mail
- Gmail SMTP

### API Documentation

- Swagger UI
- ReDoc

### Server

- Uvicorn

---

# 📂 Project Structure

```text
backend/
│
├── alembic/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone <repository-url>
```

Go to backend folder

```bash
cd backend
```

Create Virtual Environment

```bash
python -m venv env
```

Activate Virtual Environment

### Windows

```bash
env\Scripts\activate
```

### Linux / macOS

```bash
source env/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🌍 Environment Variables

Create a **.env** file in the project root.

Example:

```env
DATABASE_URL=postgresql://username:password@host:6543/database

DIRECT_URL=postgresql://username:password@host:5432/database

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

SUPABASE_URL=https://your-project.supabase.co

SUPABASE_KEY=your_supabase_anon_key

SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

MAIL_USERNAME=your-email@gmail.com

MAIL_PASSWORD=your-app-password

MAIL_FROM=your-email@gmail.com

MAIL_PORT=587

MAIL_SERVER=smtp.gmail.com

MAIL_STARTTLS=True

MAIL_SSL_TLS=False
```

---

# 🗄 Database Migration

Create Migration

```bash
alembic revision --autogenerate -m "Initial Migration"
```

Apply Migration

```bash
alembic upgrade head
```

---

# ▶️ Run Server

```bash
python -m uvicorn app.main:app --reload
```

Server

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# 🔑 Authentication

Protected APIs require a valid JWT Access Token.

Example:

```
Authorization: Bearer <access_token>
```

---

# 📦 API Modules

- Authentication
- Users
- Candidate Profile
- Recruiter Profile
- Company
- Jobs
- Applications
- Resume Upload
- Profile Image Upload
- Company Logo Upload
- Interviews
- Dashboard

---

# ☁️ Supabase Integration

This project uses **Supabase** for both database and cloud storage.

### PostgreSQL Database

- User Management
- Candidate Profiles
- Recruiters
- Companies
- Jobs
- Applications
- Interviews

### Supabase Storage

- Candidate Resume Storage
- Candidate Profile Images
- Company Logo Storage

All uploaded files are stored securely and public URLs are generated for easy access.

---

# 📧 Email Service

FastAPI Mail is used for email functionality.

Supported Features:

- Welcome Emails
- Interview Notifications
- Application Status Notifications

---



# 👨‍💻 Developer

**Rakesh Hiray**

Master of Computer Science

Backend Developer

### Skills

- FastAPI
- Python
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT Authentication
- Supabase
- React
- TypeScript

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.