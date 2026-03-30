import os
from twilio.rest import Client

def send_whatsapp_alert(to_number, current_price, target_price):
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    from_whatsapp = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    msg = f"🚨 *Gold Price Alert!* 🚨\n\nGold has hit ₹{current_price:.2f} per 10g, crossing your target of ₹{target_price:.2f}!"
    
    try:
        message = client.messages.create(
            body=msg,
            from_=from_whatsapp,
            to=f"whatsapp:{to_number}"
        )
        print(f"Alert sent to {to_number}: {message.sid}")
    except Exception as e:
        print(f"Failed to send alert: {e}")