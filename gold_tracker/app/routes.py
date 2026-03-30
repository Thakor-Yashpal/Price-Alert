from flask import render_template, request, jsonify
from app import db
from app.models import PriceHistory, AlertUser
from flask import current_app as app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/price')
def get_price_data():
    # Get last 20 price points for the chart
    history = PriceHistory.query.order_by(PriceHistory.timestamp.desc()).limit(20).all()
    history.reverse() # Chronological order
    
    if not history:
        return jsonify({"current_price": 0, "history": []})
        
    return jsonify({
        "current_price": history[-1].price_inr_10g,
        "history": [item.to_dict() for item in history]
    })

@app.route('/api/subscribe', methods=['POST'])
def subscribe_alert():
    data = request.json
    phone = data.get('phone')
    target = data.get('target')
    
    if not phone or not target:
        return jsonify({"error": "Missing data"}), 400
        
    # Standardize phone format (strip spaces, ensure + prefix)
    phone = phone.replace(" ", "")
    if not phone.startswith("+"):
        phone = "+" + phone
        
    user = AlertUser.query.filter_by(phone_number=phone).first()
    if user:
        user.target_price = float(target)
        user.is_active = True
    else:
        user = AlertUser(phone_number=phone, target_price=float(target))
        db.session.add(user)
        
    db.session.commit()
    return jsonify({"message": "Alert set successfully!"})

import requests
from flask import jsonify

@app.route('/api/news')
def get_gold_news():
    # Replace with your own free key from newsapi.org
    API_KEY = 'your_news_api_key' 
    url = f'https://newsapi.org/v2/everything?q=gold+price+market&language=en&sortBy=publishedAt&pageSize=3&apiKey={API_KEY}'
    
    try:
        response = requests.get(url)
        articles = response.json().get('articles', [])
        return jsonify(articles)
    except Exception as e:
        return jsonify([])