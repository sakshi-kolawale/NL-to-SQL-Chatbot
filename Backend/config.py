import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyB58AjQk63uzuGLIH56TyZV9n5V33y9CVQ')
    DATABASE_TYPE = 'mysql'
    DATABASE_URL = os.getenv('DATABASE_URL', 'mysql://root:root@localhost:3306/company_db')
    SECRET_KEY = os.getenv('SECRET_KEY', '8c7b9f3e2d5a4c1f7e6d9b8a2f5c3e1d9a7b6f4e8c5d2a1f3b7e9c6d4f2a8b9')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'


# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
#     DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')
#     DATABASE_URL = os.getenv('DATABASE_URL', 'database.db')
#     SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')