from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import sys
import os

# Initialize these BEFORE importing services
db = SQLAlchemy()
scheduler = APScheduler()

def create_app():
    # 1. Path Setup
    sys.path.append(os.getcwd())
    from config import Config

    # 2. Flask App Initialization with Instance Path support
    # We use instance_relative_config to keep the DB file in a dedicated folder
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # 3. Ensure the Instance Folder exists (CRITICAL for Render/Deployment)
    # Without this, SQLite may fail to create the .db file on a fresh server
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 4. Initialize Extensions
    db.init_app(app)
    
    # Only initialize and start scheduler if not in a "reloader" process
    # This prevents the "Scheduler already running" error seen in your terminal
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        scheduler.init_app(app)

    with app.app_context():
        # 5. Import Models and Routes
        from app import routes, models
        
        # Create database tables if they don't exist
        db.create_all()
        
        # 6. Setup Background Tasks
        from app.services.gold_api import fetch_and_process_gold_price
        
        # Check if job exists before adding to avoid duplicates on restart
        if not scheduler.get_job('fetch_gold'):
            scheduler.add_job(
                id='fetch_gold', 
                func=fetch_and_process_gold_price, 
                trigger='interval', 
                minutes=10
            )
        
        # Start scheduler if it isn't already active
        if not scheduler.running:
            scheduler.start()

    return app