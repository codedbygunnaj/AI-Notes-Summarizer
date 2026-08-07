import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_verification_email(email: str, verification_link: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Verify your Dhvani Account"
    msg["From"] = f"Dhvani App <{GMAIL_ADDRESS}>"
    msg["To"] = email

    html_content = f"""
        <h2>Welcome to Dhvani!</h2>
        <p>Click below to verify your email.</p>
        <a href="{verification_link}">
            Verify Email
        </a>
        <p>This link expires in one hour.</p>
    """
    
    part = MIMEText(html_content, "html")
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, email, msg.as_string())