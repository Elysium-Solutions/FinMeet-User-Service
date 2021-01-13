from flask_restplus import Resource
from User_Service import db_session, app, api
from User_Service.models.database.sql_models import User
from flask_login import login_required, current_user, login_user
import User_Service.namespaces.client_namespace.payloads
from . import payloads
from flask import request

from datetime import date, timedelta
class Login_Api(Resource):
    '''endpoint for login'''

    def post(self):
        if current_user.is_authenticated:
            return '200 Already Authenticated', 200
        login_schema = payloads.Login_Schema()
        print(request.values)
        print(request.data)
        print(request.form)
        print(api.payload)
        print(request.headers.get('cookie'))
        print(request.headers)
        data = login_schema.load(api.payload)
        temp_user = db_session.query(User).filter_by(email=data.email, active=True).first()
        if temp_user is None or not temp_user.check_password(data.password):
            return '401 Invalid Crdientials', 401

        login_user(temp_user)
        user = payloads.User(
            code=current_user.code,
            firstname=current_user.firstname,
            lastname=current_user.lastname,
            email=current_user.email,
            birthday=current_user.birthday,
            age=float((date.today() - current_user.birthday) // timedelta(days=365.2425))
        )
        user_schema = payloads.User_Schema()
        return user_schema.dump(user), 200

class Get_User_Code_Api(Resource):
    '''endpoint for logout'''
    @login_required
    def post(self):
        if current_user.is_authenticated:
            user_code = payloads.User_Code(
                User_Code=current_user.code
            )
            user_code_schema = payloads.User_Code_Schema()
            return user_code_schema.dump(user_code), 200
        return 'You are not authenticated', 401



class Logout_Api(Resource):
    '''endpoint for logout'''
    @login_required
    def post(self):
        logout_user()
        return 'You are no longer authenticated', 200

class Signup_Api(Resource):
    '''endpoint for signup'''

    def post(self):
        if current_user.is_authenticated:
            abort(405)
        signup_schema = payloads.Signup_Schema()
        data = signup_schema.load(api.payload)
        temp_user = db_session.query(User).filter_by(email=data.email).first()  
        if temp_user is None:
            new_user = User(
                firstname=data.firstname,
                lastname=data.lastname,
                email=data.email,
                birthday=data.birthday,
                password=data.password,
                phone=data.phone, 
            )
            db_session.add(new_user)
            db_session.commit()
            login_user(new_user)
            stripeCustomerObject = stripe.Customer.retrieve(current_user.stripe_customer_id)
            
            path = os.path.join(app.static_folder, os.path.join('Default_Imgs', 'Blank_Profile_Img.jpg'))
            profiles_img_bucket.delete_key(new_user.code)
            k = Key(profiles_img_bucket)
            k.key = new_user.code
            k.set_contents_from_filename(path,
                policy="public-read")

            user = payloads.User(
                code=current_user.code,
                firstname=current_user.firstname,
                lastname=current_user.lastname,
                email=current_user.email,
                birthday=current_user.birthday,
                age=float((date.today() - current_user.birthday) // timedelta(days=365.2425))
            )
            user_schema = payloads.User_Schema()
            return user_schema.dump(user), 200
        return '200 Account Already Exists', 200
