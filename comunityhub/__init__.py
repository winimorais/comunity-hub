from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '353b63f85b8497def16c8e8c55db225a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunity.db'

database = SQLAlchemy(app)

from comunityhub import routes
