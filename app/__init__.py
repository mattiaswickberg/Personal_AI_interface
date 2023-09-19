from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object('config')  # Assuming you have basic configurations in config.py
app.config['LOGIN_VIEW'] = 'login'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # specify the login route

from app import routes
