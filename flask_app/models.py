from flask_login import UserMixin
from . import db, login_manager

from datetime import datetime

class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True, min_length=1, max_length=40)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()
    
    def get_id(self):
        return str(self.id)

class Moment(db.Document):
    content = db.StringField(required=True)
    username = db.StringField(required=True)
    addressed_to = db.StringField()
    created_at = db.DateTimeField(required=True, default=datetime.now)
    location = db.ListField(db.FloatField(), default=[0.0, 0.0])
    
    meta = {
        'indexes': ['-created_at']
    }
    
    def get_id(self):
        return str(self.id)

class Comment(db.Document):
    content = db.StringField(required=True)
    username = db.StringField(required=True)
    moment_id = db.StringField(required=True)
    created_at = db.DateTimeField(required=True, default=datetime.now)
    
    meta = {
        'indexes': ['-created_at']
    }
    
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id).first()

