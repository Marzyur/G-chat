from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
load_dotenv()
import os

app=Flask(__name__,template_folder='templates')
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = app.config['SECRET_KEY']





db=SQLAlchemy(app)

migrate=Migrate(app,db)
login_manager=LoginManager()
login_manager.login_view='login'
login_manager.login_message="please login to access this page"

login_manager.init_app(app)




from app import routes,models
