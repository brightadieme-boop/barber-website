from flask import Flask, render_template, request, redirect, url_for, flash
import os
import resend
from dotenv import load_dotenv

load_dotenv()

# Create Flask app
app = Flask(__name__)
app.secret_key = "supersecretkay"

# Setup Resend
resend.api_key = os.getenv("RESEND_API_KEY")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

# ============================================
# EMAIL FUNCTIONS
# ============================================

def send_customer_confirmation(name, email, service, date):
    """Sends a beautiful confirmation email to the customer."""
    params = {
        "from": "onboarding@resend.dev",
        "to": email,
        "subject": f"✅ Booking Confirmed — Jhonny's Barber Shop",
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0d0d0d; color: #f5f5f5; border-radius: 12px; overflow: hidden;">

            <!-- Header -->
            <div style="background: #e63946; padding: 32px; text-align: center;">
                <h1 style="margin: 0; font-size: 28px; letter-spacing: 2px;">✂️ JHONNY'S</h1>
                <p style="margin: 4px 0 0; font-size: 14px; opacity: 0.9; letter-spacing: 4px;">BARBER SHOP</p>
            </div>

            <!-- Body -->
            <div style="padding: 40px 32px;">
                <h2 style="color: #e63946; margin-top: 0;">Your booking is confirmed! 🎉</h2>
                <p style="color: #ccc; line-height: 1.6;">Hey <strong style="color: #fff;">{name}</strong>, we've got you booked in. Here are your appointment details:</p>

                <!-- Booking Details Box -->
                <div style="background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 24px; margin: 24px 0;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 10px 0; color: #888; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; border-bottom: 1px solid #222;">Service</td>
                            <td style="padding: 10px 0; color: #fff; font-weight: bold; text-align: right; border-bottom: 1px solid #222;">{service}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px 0; color: #888; font-size: 13px; letter-spacing: 1px; text-transform: uppercase;">Date</td>
                            <td style="padding: 10px 0; color: #e63946; font-weight: bold; text-align: right; font-size: 18px;">{date}</td>
                        </tr>
                    </table>
                </div>

                <p style="color: #ccc; line-height: 1.6;">Please arrive <strong style="color: #fff;">5 minutes early</strong>. If you need to cancel or reschedule, please give us at least 24 hours notice.</p>

                <!-- WhatsApp Button -->
                <div style="display: flex; gap: 12px; margin-top: 24px;">
                    <a href="https://wa.me/447700000000" style="background: #25D366; color: #000; padding: 14px 32px; border-radius: 6px; text-decoration: none; font-weight: bold; letter-spacing: 1px; font-size: 14px;">📱 Message Us on WhatsApp</a>
                </div>

                <p style="color: #666; font-size: 13px; text-align: center;">See you soon, {name}! ✂️</p>
            </div>

            <!-- Footer -->
            <div style="background: #111; padding: 20px 32px; text-align: center; border-top: 1px solid #222;">
                <p style="color: #555; font-size: 12px; margin: 0;">© Jhonny's Barber Shop · London</p>
            </div>
        </div>
        """
    }
    resend.Emails.send(params)


def send_admin_notification(name, email, service, date):
    """Sends instant notification to the barber when someone books."""
    params = {
        "from": "onboarding@resend.dev",
        "to": ADMIN_EMAIL,
        "subject": f"🔔 NEW BOOKING — {name} wants a {service} on {date}",
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">

            <!-- Alert Header -->
            <div style="background: #ff6b00; padding: 20px 32px; display: flex; align-items: center;">
                <h1 style="margin: 0; color: #000; font-size: 20px; letter-spacing: 1px;">🔔 NEW BOOKING ALERT</h1>
            </div>

            <!-- Details -->
            <div style="background: #1a1a1a; padding: 32px;">
                <p style="color: #aaa; margin-top: 0;">Someone just booked through your website. Here are the full details:</p>

                <div style="background: #111; border: 1px solid #333; border-radius: 8px; padding: 24px; margin: 16px 0;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid #222;">
                            <td style="padding: 12px 0; color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">👤 Customer Name</td>
                            <td style="padding: 12px 0; color: #fff; font-weight: bold; text-align: right; font-size: 18px;">{name}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #222;">
                            <td style="padding: 12px 0; color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">📧 Their Email</td>
                            <td style="padding: 12px 0; color: #ff6b00; text-align: right;">{email}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #222;">
                            <td style="padding: 12px 0; color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">✂️ Service</td>
                            <td style="padding: 12px 0; color: #fff; text-align: right;">{service}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">📅 Appointment Date</td>
                            <td style="padding: 12px 0; color: #ff6b00; font-weight: bold; text-align: right; font-size: 24px;">{date}</td>
                        </tr>
                    </table>
                </div>

                <!-- Action buttons -->
                <div style="display: flex; gap: 12px; margin-top: 24px;">
                    <a href="mailto:{email}" style="background: #ff6b00; color: #000; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 13px;">📧 Reply to Customer</a>
                    <a href="https://wa.me/447700000000" style="background: #25D366; color: #000; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 13px;">📱 WhatsApp Them</a>
                </div>

                <p style="color: #444; font-size: 12px; margin-top: 24px; border-top: 1px solid #222; padding-top: 16px;">
                    ✅ Booking saved to your booking.csv automatically.<br>
                    ✅ Customer confirmation email sent to {email}.
                </p>
            </div>
        </div>
        """
    }
    resend.Emails.send(params)


# ============================================
# ROUTES
# ============================================

# #1 Home page route
@app.route('/')
def home():
    return render_template('index.html')

# #2 Booking page route
@app.route('/booking')
def booking():
    return render_template('booking.html')

# #3 Handle booking form submissions
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    service = request.form['service']
    date = request.form['date']

    # Save to CSV
    with open('booking.csv', 'a') as f:
        f.write(f"{name},{email},{service},{date}\n")

    # Send emails
    try:
        send_customer_confirmation(name, email, service, date)
        send_admin_notification(name, email, service, date)
    except Exception as e:
        print(f"Email error: {e}")

    flash(f"Booking confirmed for {name} on {date} for a {service}. We'll email you at {email}.")
    return redirect(url_for('booking'))

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)