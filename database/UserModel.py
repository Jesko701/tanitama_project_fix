from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


class UserModel(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('database_uri')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
