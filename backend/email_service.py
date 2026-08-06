import os
import resend
import dotenv

dotenv.load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
def send_verification_email(email: str,verification_link: str):
    params = {
    "from": "Dhvani <onboarding@resend.dev>",
    "to": [email],
    "subject": "Verify your Dhvani Account",
    "html": f"""
        <h2>Welcome to Dhvani!</h2>

        <p>Click below to verify your email.</p>

        <a href="{verification_link}">
            Verify Email
        </a>

        <p>This link expires in one hour.</p>
    """
    }

    resend.Emails.send(params)