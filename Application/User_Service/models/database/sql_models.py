import uuid
from enum import Enum
from datetime import datetime, timedelta

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean, Date, Enum as DB_Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User_Types_Enum(Enum):
    client = 0
    firm = 1

class User(Base, UserMixin):
    """model for "users" table, recoard created for each new user that joins"""

    __tablename__ = 'users'
    __code_prefix__ = 'UR__'
    
    # Object referencing
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(36), primary_key=False, autoincrement=False, unique=True, nullable=False)

    # Modifcation/Creation tracking
    created_datetime = Column(DateTime(timezone=True), default=datetime.utcnow())
    modified_datetime = Column(DateTime(timezone=True), onupdate=datetime.utcnow())
    # Active record
    active = Column(Boolean, index=True, nullable=False, default=True)

    firstname = Column(String(32), index=True, nullable=False)
    lastname = Column(String(32), index=True, nullable=False)
    email = Column(String(64), index=False, nullable=False)
    phone = Column(String(12), index=False, nullable=False)
    
    phone_verified = Column(Boolean, index=False, nullable=False)
    birthday = Column(Date(), index=False, nullable=False)
    pass_hash = Column(String(128), index=False, nullable=False)


    profile_photo_url = Column(String(128), index=False, nullable=True)

    handicap_offset = Column(Integer, default=0)
    handicap_starting = Column(Integer, default=6)

    user_type = Column(DB_Enum(User_Types_Enum), index=False, nullable=False, default=User_Types_Enum.client)

    def __init__(self, firstname, lastname, email, birthday, password, phone, user_type=User_Types_Enum.client):
        code = self.__code_prefix__ + uuid.uuid4().hex
        self.code = code
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.birthday = birthday
        self.pass_hash = generate_password_hash(password)
        self.phone = phone
        self.phone_verified = False
        self.user_type = user_type


    def get_credits(self):    
        stripeCustomerObject = stripe.Customer.retrieve(current_user.stripe_customer_id)
        return stripeCustomerObject.get('balance')

    def get_number_of_attended_tournaments(self):
        total_number = 0
        for user_tournament in self.touraments:
            if user_tournament.joined == True:
                total_number+=1
        return total_number


    def generate_new_code(self):
        code = self.__code_prefix__ + uuid.uuid4().hex
        self.code = code
        return code

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)


   
