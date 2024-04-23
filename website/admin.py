from flask import Blueprint, render_template, url_for,jsonify
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import plotly.express as px
import pandas as pd
from . import db
from .models import User, AiDoctor
from flask_login import UserMixin

admin = Blueprint('admin', __name__, url_prefix='/admin')

# ... other imports

# class User(db.Model, UserMixin):
#     # ... existing user model definition
#
#     def get_ai_doctor_data(self):
#         """
#         This function retrieves all AiDoctor entries associated with the user.
#         """
#         return AiDoctor.query.filter_by(user_id=self.id).all()
#ai_doctor_entries = AiDoctor.query.filter_by().all()

# if ai_doctor_entries:
#     for entry in ai_doctor_entries:
#         print(f"Disease Ai doctor: {entry.disease}")
#         print(f"Description: {entry.description}")
#         # ... access other AiDoctor data
# else:
#     print(f"No AiDoctor entries found for user ID {user_id}")


def get_ai_doctor_entries(user_id):
    #with app.app_context():
    ai_doctor_entries = AiDoctor.query.filter_by(user_id=user_id).all()
    return ai_doctor_entries


@admin.route('/dashboard')
def dashboard():
    users = User.query.all()
    ai_doctor_entries = AiDoctor.query.filter_by().all()
    map_data = []

    for user in users:
        entries = get_ai_doctor_entries(f'{user.id}')
        for entry in entries:
            print(entry.user.username,entry.id, entry.disease, entry.description, entry.precaution, entry.medication, entry.workouts,
                  entry.diet, entry.date, entry.user_id)
        #ai=AiDoctor.query.filter_by(user_id=user.id)
        #print(f"Disease Ai doctor: {ai}")
        map_data.append({
            'location': [user.latitude, user.longitude],  # Marker location
            'popup': f"<b>{user.username}</b><br>{User.email}<br>{user.first_name}"  # User data popup
        })

    # Render template with users and map data
    return render_template('admin_dashboard.html', users=users, user=current_user, map_data=map_data)
#, map_html=map_html
from flask import jsonify

# @admin.route('/get_location')
# def get_location():
#     # Get the user
#     user = User.query.all()  # Replace this with the actual query to get the user
#
#     # Return the location data as JSON
#     return jsonify({
#         'latitude': user.latitude,
#         'longitude': user.longitude
#     })

@admin.route('/get_locations')
def get_locations():
    users = User.query.all()  # Get all users
    locations = []
    for user in users:
        if user.id != 1:
            locations.append({
                'username': user.username,
                'latitude': user.latitude,
                'longitude': user.longitude,
                'details': user.first_name # Replace with actual user details
            })
    return jsonify(locations)

@admin.route('/users')#http://127.0.0.1:5000/users
def users():
    # Fetch users from the database
    users = User.query.all()
    return render_template('users.html', users=users,user=current_user)

@admin.route('/diseases')
def diseases():
    # Fetch diseases from the database
    users = User.query.all()
    for user in users:
        entries = get_ai_doctor_entries(f'{user.id}')
    # diseases = Disease.query.all()
    return render_template('diseases.html', entries=entries, users=users, user=current_user)


@admin.route('/vitals')
def vitals():
    # Fetch vital signs from the database
    # vitals = VitalSign.query.all()
    # return render_template('vitals.html', vitals=vitals)
    pass
