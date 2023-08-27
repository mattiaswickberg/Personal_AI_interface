import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLAlchemy configurations
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://testuser:test@localhost/ai_chatbot'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY')
