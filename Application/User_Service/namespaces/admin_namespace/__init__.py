from flask_restplus import Namespace, Api
from .endpoints import 

admin_namespace = Namespace(name='Admin Namespace', path='/admin', description='Contains endpoints that correspond with user admins, and allows admins to securely create and managment tours/tournaments')

