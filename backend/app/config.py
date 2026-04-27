import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-123'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/technical_database'
    MONGO_TEST_URI = os.environ.get('MONGO_TEST_URI') or 'mongodb://localhost:27017/test_technical_database'
    JWT_SECRET = os.environ.get('JWT_SECRET') or 'jwt-secret-key-456'
    JWT_EXPIRY_HOURS = int(os.environ.get('JWT_EXPIRY_HOURS') or 24)
