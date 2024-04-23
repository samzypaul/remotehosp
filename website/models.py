from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import json
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AiDoctor(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    disease = db.Column(db.String(100))
    description = db.Column(db.String(300))
    precaution =db.Column(db.String(600))
    medication = db.Column(db.String(300))
    workouts = db.Column(db.String(300))
    diet = db.Column(db.String(300))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref="AiDoctor")


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    latitude = db.Column(db.DECIMAL(10, 6))
    longitude = db.Column(db.DECIMAL(10, 6))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    aidoctor = db.relationship('AiDoctor')

# class AiDoctor(Base):
#       __tablename__ = 'patient_health_data'
#
#       id = Column(Integer, primary_key=True)
#       disease = Column(String(100))
#       description = Column(String(300))
#       precaution = Column(String(600))
#       medication = Column(String(300))
#       workouts = Column(Text(300))  # Assuming workouts can be serialized to JSON string
#       diet = Column(Text(300))  # Assuming diet can be serialized to JSON string
#       date = Column(DateTime(timezone=True), default=func.now)
#       # Assuming a separate User model exists
#       user_id = Column(Integer, ForeignKey('user.id'))
#       user = Base.relationship("User", backref="health_data")