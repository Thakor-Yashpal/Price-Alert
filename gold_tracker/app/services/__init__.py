from .gold_api import fetch_and_process_gold_price
from .twilio_service import send_whatsapp_alert

def check_and_alert():
    gold = get_gold_price()
    silver = get_silver_price()
    diamond = get_diamond_price()

    users = User.query.all()

    for user in users:
        message = ""

        if gold < user.gold_threshold:
            message += f"Gold ↓ ₹{gold:.2f}\n"

        if silver < user.silver_threshold:
            message += f"Silver ↓ ₹{silver:.2f}\n"

        if diamond < user.diamond_threshold:
            message += f"Diamond ↓ ₹{diamond:.2f}\n"

        if message:
            send_whatsapp(user.phone, "🚨 Price Alert:\n" + message)
            
last_prices = {"gold": None}

def check_and_alert():
    gold = get_gold_price()

    if last_prices["gold"]:
        change = ((last_prices["gold"] - gold) / last_prices["gold"]) * 100

        if change > 2:  # 2% drop
            send_whatsapp(user.phone, f"⚠️ Gold dropped {change:.2f}% → ₹{gold}")

    last_prices["gold"] = gold