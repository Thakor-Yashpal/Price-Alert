import os
import requests
from flask import current_app

def fetch_and_process_gold_price():
    from app import db
    from app.models import PriceHistory, AlertUser
    from .twilio_service import send_whatsapp_alert

    headers = {
        "x-access-token": os.getenv("GOLD_API_KEY"),
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get("https://www.goldapi.io/api/XAU/INR", headers=headers)
        data = response.json()
        
        if 'error' in data:
            print(f"API Error: {data['error']}")
            return

        price_per_ounce = data.get('price')
        if price_per_ounce:
            # --- THE NEW MATH SECTION ---
            base_price_10g = (price_per_ounce / 31.1034768) * 10
            
            # 9% Import Duty + 3% GST + ~1% Local Premium = 1.13 total multiplier
            # This should bring 1,34,000 up to ~1,51,400
            indian_market_multiplier = 1.13 
            
            current_price = round(base_price_10g * indian_market_multiplier, 2)
            # ----------------------------

            print(f"💰 New Local Price Calculated: ₹{current_price}")
            
            new_entry = PriceHistory(price_inr_10g=current_price)
            db.session.add(new_entry)
            db.session.commit()
            
            # Alert check
            users = AlertUser.query.filter_by(is_active=True).all()
            for user in users:
                if current_price <= user.target_price:
                    send_whatsapp_alert(user.phone_number, current_price, user.target_price)
            
    except Exception as e:
        print(f"Error in gold_api: {e}")