import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLAlchemy configurations
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY')
