from .extensions import db
from flask_login import UserMixin
from datetime import datetime

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default= datetime.utcnow)
    slug = db.Column(db.String(255))
    poster_id= db.Column(db.Integer, db.ForeignKey('users.id'))

class Users(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True )
    username = db.Column(db.String(20), nullable=False, unique=True)
    name=db.Column(db.String(200), nullable=False)
    email=db.Column(db.String(120), nullable=False, unique=True)
    about_me=db.Column(db.Text(500), nullable=True)
    profile_pic=db.Column(db.String(120), nullable=True)
    date_added=db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(150))
    posts = db.relationship('Posts', backref='poster')

    # The serialize method converts the object to a dictionary
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "emai": self.email
        }