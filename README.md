# Schedulo
 A simple Flask-based appointment booking system with email confirmations, QR code access, and automated reminder scheduling.


# 📅 Appointment Booking System with QR & Email Notifications

This is a **Flask-based Appointment Booking Web App** that allows users to schedule appointments via a web interface. It features automatic email confirmations, QR code generation, a slot viewer, and automated reminder emails the night before appointments.

---

## 🚀 Features

- 🖥️ Simple & responsive web form to book appointments  
- 📧 Sends confirmation email to users instantly  
- 📲 Generates a scannable QR code linking to the booking page  
- 📋 View all booked slots via a dedicated page  
- ⏰ Automated reminder emails to client and admin the night before appointment  
- 🗃️ SQLite database for lightweight and easy data storage  

---

## 🛠️ Tech Stack

- **Python** (Flask)
- **SQLite** (for database)
- **HTML/CSS** (frontend)
- **smtplib / Gmail SMTP** (for email notifications)
- **qrcode** (Python QR code generation)
- **dotenv** (to keep credentials secure)

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/appointment-booking-system.git
cd appointment-booking-system
pip install flask qrcode python-dotenv
