from email.policy import default

from flask_login import LoginManager

from comunityhub import database, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin
import humanize


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def current_utc_time():
    return datetime.now(timezone.utc)


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    profile_photo = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='author', lazy=True)
    courses = database.Column(database.String, nullable=False, default='None')

    def posts_count(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    body = database.Column(database.Text, nullable=False)
    posted_on = database.Column(database.DateTime, nullable=False, default=current_utc_time)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    @property
    def posted_on_humanized(self):
        if self.posted_on.tzinfo is None:
            posted_on_aware = self.posted_on.replace(tzinfo=timezone.utc)
        else:
            posted_on_aware = self.posted_on
        return humanize.naturaltime(current_utc_time() - posted_on_aware)
