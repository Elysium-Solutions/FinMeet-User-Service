from flask_restplus import Resource, fields, inputs
from dataclasses import dataclass
from typing import List
import datetime
import marshmallow_dataclass
import marshmallow.validate

@dataclass
class Plaid_Link_Token:
    Plaid_Link_Token : str
    Access_Token_Ref_Code : str

Plaid_Link_Token_Schema = marshmallow_dataclass.class_schema(Plaid_Link_Token)

@dataclass
class User_Code:
    User_Code : str

User_Code_Schema = marshmallow_dataclass.class_schema(User_Code)

@dataclass
class Plaid_Access_Token:
    User_Code : str
    Access_Token_Ref_Code : str
    Access_Token : str
    Item_Id : str

User_Code_Schema = marshmallow_dataclass.class_schema(Plaid_Access_Token)


@dataclass
class Plaid_Account:
    name : str
    official_name : str
    subtype : str
    account_id : str
    available : int
    current : int
    iso_currency_code : str

Plaid_Account_Schema = marshmallow_dataclass.class_schema(Plaid_Account)

@dataclass
class Plaid_Account_List:
    Accounts : List[Plaid_Account]

Plaid_Account_List_Schema = marshmallow_dataclass.class_schema(Plaid_Account_List)

@dataclass
class Login:
    email : str
    password : str

Login_Schema = marshmallow_dataclass.class_schema(Login)


@dataclass
class User:
    '''General Marshmallow user model'''
    code : str = None
    firstname : str = None
    lastname : str = None
    email : str = None
    birthday : datetime.date = None
    age : int = None
    
User_Schema = marshmallow_dataclass.class_schema(User)


@dataclass
class Signup:
    firstname : str
    lastname : str
    email : str
    password : str
    phone : str
    birthday : datetime.date    


Signup_Schema = marshmallow_dataclass.class_schema(Signup)
