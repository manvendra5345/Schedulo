from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import qrcode
import io
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']

        # Store in database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO appointments (name, email, date, time) VALUES (?, ?, ?, ?)',
                       (name, email, date, time))
        conn.commit()
        conn.close()

        # Send confirmation email to the client
        subject = "Appointment Confirmation"
        body = f"Hello {name},\n\nYour appointment is confirmed for {date} at {time}.\n\nThank you!"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
        except Exception as e:
            print(f"Error sending confirmation email: {e}")

        return redirect(url_for('success'))

    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')  # Nice UI page

@app.route('/qr')
def qr():
    qr_url = "http://192.168.0.105:5000/"  # Replace with public IP/domain when deployed
    img = qrcode.make(qr_url)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/slots')
def slots():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, time, name FROM appointments')
    rows = cursor.fetchall()
    conn.close()
    return render_template('slots.html', appointments=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
