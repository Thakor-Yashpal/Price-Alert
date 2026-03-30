import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///goldtracker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_ENABLED = True