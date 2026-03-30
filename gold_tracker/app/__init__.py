from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import sys
import os

# Initialize these BEFORE importing services
db = SQLAlchemy()
scheduler = APScheduler()

def create_app():
    # Ensure root is in path for config
    sys.path.append(os.getcwd())
    from config import Config

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    scheduler.init_app(app)

    with app.app_context():
        # Models and routes must be imported here
        from app import routes, models
        db.create_all()
        
        # IMPORT SERVICE HERE (Inside the context, not at the top of the file)
        from app.services.gold_api import fetch_and_process_gold_price
        
        if not scheduler.get_job('fetch_gold'):
            scheduler.add_job(id='fetch_gold', func=fetch_and_process_gold_price, trigger='interval', minutes=10)
        
        if not scheduler.running:
            scheduler.start()

    return app