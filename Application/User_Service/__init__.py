import os, json
from flask import Flask
from sqlalchemy import create_engine
from flask_marshmallow import Marshmallow
from flask_restplus import Api
from User_Service.config import Config
import datetime
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS
from flask_login import LoginManager

path = os.path.join(os.getcwd(), os.path.join('configs', 'app_settings.Config'))
with open(path) as config_file:
    app_config = json.load(config_file)

config = Config.get_instance()

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = config.SECRET_KEY


app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ADDRESS'] = config.ADDRESS
app.config['BALANCE_WEBHOOK_URL'] = config.BALANCE_WEBHOOK_URL


from .models.database.sql_models import User, Base

# SQLALCHEMY Setup
db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

# create metadata
Base.metadata.create_all(db_engine)

# create session
Session = sessionmaker(bind=db_engine)
db_session = Session()

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)


from User_Service.models.auth_models import auth_models

ma = Marshmallow(app)


api = Api(app)

CORS(app, resources={'/*': {'origins': '*'}})

from .namespaces.client_namespace import client_namespace

api.add_namespace(client_namespace)



@app.after_request
def after_request(response):    
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# Here we patch the application
from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)