from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime

#adding flask security Passwords
from werkzeug.security import generate_password_hash, check_password_hash

#import for secrets module (given by python)
import secrets

#Imports for login-manager
from flask_login import UserMixin

#import for flask login
from flask_login import LoginManager

#import for flask marshmallow
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# make sure to add un user mixin to user class
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    skate = db.relationship('Skate', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added to the database!"



class Skate(db.Model):
    id = db.Column(db.String, primary_key = True)
    deck_brand = db.Column(db.String(150))
    grip_tape = db.Column(db.String(150))
    trucks = db.Column(db.String(150))
    wheels = db.Column(db.String(150))
    bearings = db.Column(db.String(150))
    hardware = db.Column(db.String(150))
    price = db.Column(db.Numeric(precision=5, scale=2))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)


    def __init__(self, deck_brand, grip_tape, trucks, wheels, bearings, hardware, price, user_token, id = ''):
        self.id = self.set_id()
        self.deck_brand = deck_brand
        self.grip_tape = grip_tape
        self.trucks = trucks
        self.wheels = wheels
        self.bearings = bearings
        self.hardware = hardware
        self.price = price
        self.user_token = user_token


    def __repr__(self):
        return f"The following Skateboard has been added: {self.deck_brand}"

    def set_id(self):
        return (secrets.token_urlsafe())


#Creation of API schema via the marshmallow object
class SkateSchema(ma.Schema):
    class Meta:
        fields = ['id','deck_brand','grip_tape','trucks','wheels','bearings','hardware','price']

skate_schema = SkateSchema()
skates_schema = SkateSchema(many = True)