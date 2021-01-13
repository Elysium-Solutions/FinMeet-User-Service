from flask_restplus import Namespace, Api
from .endpoints import Login_Api, Logout_Api, Signup_Api, Get_User_Code_Api

client_namespace = Namespace(name='Client Namespace', path='/client', description='Contains endpoints that correspond with user client')

client_namespace.add_resource(Login_Api, '/login')
client_namespace.add_resource(Logout_Api, '/logout')
client_namespace.add_resource(Signup_Api, '/signup')
client_namespace.add_resource(Get_User_Code_Api, '/user_code_get')
