import os
from dotenv import load_dotenv
from dotenv import load_dotenv
load_dotenv()

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'mysql')
    DATABASE_URL = os.getenv('DATABASE_URL', 'mysql://root:root@localhost:3306/company_db')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'



