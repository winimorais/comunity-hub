from comunityhub import database
from datetime import datetime, timezone

def current_utc_time():
    return datetime.now(timezone.utc)

class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Columng(database.String, nullable=False)
    profile_photo = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='writer', lazy=True)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    body = database.Column(database.Text, nullable=False)
    posted_on = database.Column(database.DateTime, nullable=False, default=current_utc_time)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)