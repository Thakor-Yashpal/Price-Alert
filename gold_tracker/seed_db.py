from app import create_app, db
from app.models import PriceHistory
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    # Add 5 fake price points to see the chart and price
    base_price = 62500.0
    for i in range(5):
        test_price = PriceHistory(
            price_inr_10g = base_price + (i * 150),
            timestamp = datetime.utcnow() - timedelta(minutes=(5-i)*10)
        )
        db.session.add(test_price)
    
    db.session.commit()
    print("✅ Success! Database seeded with 5 test prices. Refresh your browser.")