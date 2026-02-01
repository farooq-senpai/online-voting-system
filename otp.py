import random
import string
import smtplib
from email.mime.text import MIMEText
from flask import current_app

# Simple in-memory storage for OTPs (In production, use Redis or DB with expiry)
otp_storage = {} 

def generate_otp():
    """Generates a 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=6))

def send_otp(email, otp):
    print(f"[MOCK OTP] {email} -> {otp}")
    return
    """Sends OTP via email. Falls back to mock print if credentials missing."""
    username = current_app.config['MAIL_USERNAME']
    password = current_app.config['MAIL_PASSWORD']

    if not username or not password:
        print(f"[{'='*30}]")
        print(f"MOCK OTP for {email}: {otp}")
        print(f"[{'='*30}]")
        return True

    try:
        msg = MIMEText(f'Your OTP for Online Voting System is: {otp}\n\nThis OTP is valid for 5 minutes.')
        msg['Subject'] = 'Verify your Account - Online Voting System'
        msg['From'] = username
        msg['To'] = email

        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def store_otp(email, otp):
    """Stores OTP with the email."""
    # TODO: Add timestamp for expiry check
    otp_storage[email] = otp

def verify_otp_logic(email, user_otp):
    """Verifies the provided OTP."""
    if email in otp_storage and otp_storage[email] == user_otp:
        del otp_storage[email] # Clear after use
        return True
    return False
