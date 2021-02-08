from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from models import User, Post
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_PROJECT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
import routes, models
