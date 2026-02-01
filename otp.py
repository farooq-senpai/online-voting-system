import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")


def send_otp_email(to_email, otp):
    if not SENDGRID_API_KEY or not FROM_EMAIL:
        print("[SendGrid] Missing API key or sender email")
        return False

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="Your OTP Verification Code",
        html_content=f"""
        <h2>Online Voting System</h2>
        <p>Your One-Time Password (OTP) is:</p>
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
