# 🗳️ Online Voting System (OVS)

A secure and modern **Online Voting System** built using **Python Flask**, designed for real-time voting with role-based access, OTP email verification, and a clean UI.  
This project demonstrates full-stack backend skills, authentication workflows, and cloud deployment.

🔗 **Live Demo:**  
👉 https://online-voting-system-production-a578.up.railway.app/

---

## ✨ Features

### 👥 User Roles
- **Voter**
  - Register & login
  - Receive OTP via email
  - Vote only once
- **Political Party**
  - Login securely
  - View real-time vote count

### 🔐 Authentication & Security
- Secure password hashing
- Email OTP verification (SendGrid)
- Session-based authentication
- One-user-one-vote enforcement

### 📩 Email Verification
- OTP sent using **SendGrid Email API**
- Cloud-safe (no SMTP issues)
- Graceful fallback if email fails

### 📊 Voting System
- Minimum of 8 parties supported
- Real-time vote updates
- Vote locking after submission

### 🎨 User Interface
- Modern gradient-based UI
- Responsive design (desktop & mobile)
- Clean dashboard layout
- Animated buttons & hover effects

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|------------|
| Backend | Python, Flask |
| Auth | Flask-Login |
| Database | SQLite |
| ORM | SQLAlchemy |
| Email | SendGrid API |
| Frontend | HTML, CSS |
| Deployment | Railway |
| Server | Gunicorn |

---

## 📁 Project Structure

online-voting-system/
│
├── main.py # App entry point
├── auth.py # Authentication & OTP routes
├── voting.py # Voting logic
├── otp.py # OTP generation & verification
├── models.py # Database models
├── config.py # App configuration
├── requirements.txt
│
├── templates/ # HTML templates
└── static/ # CSS & assets


---

## ⚙️ Environment Variables

The following environment variables are required (configured on Railway):

```env
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=your_verified_email@gmail.com
ENV=production
🚀 Deployment
This project is deployed on Railway using:

gunicorn main:app
Production-ready setup

Automatic redeploy on GitHub push

Public domain provided by Railway

🧪 How It Works (Flow)
User registers (Voter / Party)

OTP is generated and emailed

User verifies OTP (or logs in with limited access)

Voter accesses voting booth

Vote is cast (only once)

Parties see real-time results

📸 Screenshots
(You can add screenshots here later)

🎓 Project Purpose
This project was built to:

Practice full-stack Flask development

Understand authentication & authorization

Integrate real email services

Learn cloud deployment & debugging

Build an interview-ready real-world project

🔮 Future Improvements
Resend OTP feature

OTP expiry countdown

Admin dashboard

PostgreSQL support

JWT-based auth

Custom domain email (no-reply@domain.com)

👨‍💻 Author
Abdul Farooq
Final-year B.Sc Computer Science Student
Passionate about backend development, AI, and system design.

⭐ Support
If you like this project:

⭐ Star the repository

🍴 Fork it

🧠 Learn from it
