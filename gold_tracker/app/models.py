from datetime import datetime
from app import db

class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price_inr_10g = db.Column(db.Float, nullable=False)
    # Ensure this stays as datetime.utcnow so the DB remains standardized
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "price": self.price_inr_10g,
            # Format the time as an ISO string so JavaScript can localise it
            "time": self.timestamp.isoformat() + "Z" 
        }
class AlertUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    