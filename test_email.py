import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

params = {
    "from": "onboarding@resend.dev",
    "to": os.getenv("ADMIN_EMAIL"),
    "subject": "✅ Barbershop Email System Working!",
    "html": """
        <h2>Your automation engine is connected! 🚀</h2>
        <p>This is the system that will power:</p>
        <ul>
            <li>✅ Booking confirmations</li>
            <li>⏰ Appointment reminders</li>
            <li>⭐ Review requests</li>
            <li>🤖 AI enquiry responses</li>
        </ul>
        <p>Let's get building!</p>
    """
}

email = resend.Emails.send(params)
print("✅ Test email sent! ID:", email["id"])