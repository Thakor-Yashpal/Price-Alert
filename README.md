# 🪙 GoldTracker Pro
### Live FinTech Dashboard with Real-Time WhatsApp Alerts

GoldTracker Pro is a modern web application designed to track 24K gold prices in the Indian market (INR) with high precision. It features a sleek, glassmorphic dashboard, real-time price charting, and an automated WhatsApp notification system for price drops.

![Dashboard Preview](https://via.placeholder.com/800x450?text=GoldTracker+Pro+Dashboard+Preview)

## ✨ Features
* **Live Price Feed:** Fetches real-time XAU/INR data via GoldAPI.io.
* **Indian Market Precision:** Automatically calculates local prices by factoring in Import Duty and GST (approx. +13%) to match local rates (e.g., Ahmedabad/Vadodara).
* **Interactive Charts:** Dynamic price history visualization using Chart.js with local IST timezone support.
* **Smart WhatsApp Alerts:** Integration with Twilio to send instant notifications when gold hits your target price.
* **Modern UI:** High-end FinTech design using glassmorphism, Lucide icons, and responsive CSS.

## 🛠️ Tech Stack
* **Backend:** Flask (Python)
* **Database:** SQLAlchemy (SQLite)
* **Task Scheduling:** Flask-APScheduler (runs every 10 minutes)
* **Frontend:** HTML5, CSS3 (Modern Glassmorphism), JavaScript (ES6)
* **APIs:** GoldAPI.io, Twilio WhatsApp Business API
