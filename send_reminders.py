from datetime import datetime, timedelta
import sqlite3
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load email credentials
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Admin email
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Get tomorrow's date
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT name, email, date, time FROM appointments WHERE date = ?', (tomorrow,))
appointments = cursor.fetchall()
conn.close()

print(f"Found {len(appointments)} appointments for tomorrow.")

# 1. Send individual reminders to users
for name, email, date, time in appointments:
    subject = "Appointment Reminder"
    body = f"Hello {name},\n\nThis is a reminder for your appointment on {date} at {time}.\n\nThank you!"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Reminder sent to {email}")
    except Exception as e:
        print(f"❌ Error sending to {email}: {e}")

# 2. Send summary to admin
if appointments:
    summary = f"📅 Appointments scheduled for {tomorrow}:\n\n"
    for name, email, date, time in appointments:
        summary += f"- {name} ({email}) at {time}\n"

    admin_msg = MIMEText(summary)
    admin_msg['Subject'] = f"Appointment Summary for {tomorrow}"
    admin_msg['From'] = EMAIL_ADDRESS
    admin_msg['To'] = EMAIL_ADDRESS  # Send to admin

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(admin_msg)
        print("✅ Summary sent to admin.")
    except Exception as e:
        print(f"❌ Error sending summary to admin: {e}")
else:
    print("ℹ️ No appointments found for tomorrow.")
