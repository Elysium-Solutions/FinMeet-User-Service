from User_Service import db_session, login_manager
from User_Service.models.database.sql_models import User
from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_header


@login_manager.user_loader
def load_user(user_code):
    temp_user = db_session.query(User).filter_by(code=user_code).first()
    return temp_user

@login_manager.request_loader
def load_user_from_request(request):

    cookie_id = request.headers.get('cookie')

    return None