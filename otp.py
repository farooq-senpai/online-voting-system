import random
import time
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# In-memory OTP store (OK for demo / college project)
OTP_STORE = {}

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")


def generate_otp():
    return str(random.randint(100000, 999999))


def store_otp(email, otp):
    OTP_STORE[email] = {
        "otp": otp,
        "timestamp": time.time()
    }


def send_otp(email, otp):
    if not SENDGRID_API_KEY or not FROM_EMAIL:
        print("[SendGrid] Missing API key or FROM_EMAIL")
        return False

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=email,
        subject="Your OTP Verification Code",
        html_content=f"""
        <h2>Online Voting System</h2>
        <p>Your OTP is:</p>
        <h1>{otp}</h1>
        <p>This OTP is valid for 5 minutes.</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return True
    except Exception as e:
        print("[SendGrid ERROR]", e)
        return False


def verify_otp_logic(email, entered_otp):
    record = OTP_STORE.get(email)

    if not record:
        return False

    # OTP valid for 5 minutes
    if time.time() - record["timestamp"] > 300:
        OTP_STORE.pop(email, None)
        return False

    if record["otp"] == entered_otp:
        OTP_STORE.pop(email, None)
        return True

    return False
