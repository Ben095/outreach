from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from werkzeug.security import generate_password_hash, \
     check_password_hash
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class Google(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    googleQuery = db.Column(db.String(200), index=True)
    googleMetaTitle = db.Column(db.String(200), index=True)
    googleFullURL = db.Column(db.String(200))
    googleRootDomain = db.Column(db.String(200))
    Links = db.Column(db.Integer)
    PA = db.Column(db.Integer)
    DA = db.Column(db.Integer)
    moz_rank = db.Column(db.Integer)
    facebook_shares = db.Column(db.Integer)
    twitter_shares = db.Column(db.Integer)
    google_shares = db.Column(db.Integer)
    
    