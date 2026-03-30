from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import sys
import os

# Initialize extensions
db = SQLAlchemy()
scheduler = APScheduler()

def create_app():
    # Ensure app can find config in subfolders
    sys.path.append(os.getcwd())
    from config import Config

    # Initialize Flask with instance folder support
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # CREATE INSTANCE FOLDER: Essential for SQLite on Render
    try:
        if not os.path.exists(app.instance_path):
            os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    
    # Initialize scheduler
    scheduler.init_app(app)

    with app.app_context():
        from app import routes, models
        db.create_all()
        
        # Background Job Setup
        from app.services.gold_api import fetch_and_process_gold_price
        
        if not scheduler.get_job('fetch_gold'):
            scheduler.add_job(
                id='fetch_gold', 
                func=fetch_and_process_gold_price, 
                trigger='interval', 
                minutes=10
            )
        
        if not scheduler.running:
            scheduler.start()

    return app