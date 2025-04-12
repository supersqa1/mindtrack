import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
    MYSQL_DB = os.getenv('MYSQL_DB', 'mindtrack')
    
    # App configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    API_KEY_LENGTH = 32
    
    # Demo data configuration
    DEMO_USER_ID = 1  # ID for demo user
    DEMO_TASK_LIFETIME_HOURS = 24  # How long demo tasks should live
