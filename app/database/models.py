from datetime import datetime
from app import db
from flask_login import UserMixin


class ConfigurationPreset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    ai_model = db.Column(db.String(120), nullable=False)
    system_prompt = db.Column(db.String(500), nullable=True)
    temperature = db.Column(db.Float, nullable=False)
    top_p = db.Column(db.Float, nullable=False)

class UserConfiguration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    user_info = db.Column(db.String(500), nullable=True)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', back_populates='role')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    chat_histories = db.relationship('ChatHistory', backref='user', lazy=True)
    summaries = db.relationship('Summary', backref='user', lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)  # Making it nullable initially to handle existing users
    role = db.relationship('Role', back_populates='users')

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, default=True)  # Default is True assuming most entries would be user messages
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
