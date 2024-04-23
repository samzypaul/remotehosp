from flask import Blueprint, render_template, url_for, jsonify
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


@admin.route('/dashboard')
def dashboard():
    users = User.query.all()

    map_data = []

    for user in users:
        ai_doctor_data = user.get_ai_doctor_data()  # Get AiDoctor data for user
        # ... existing map_data population logic

        # Add AiDoctor data to user data for template
        user_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'ai_doctor_data': ai_doctor_data  # Add AiDoctor data key
        }
        map_data.append(user_data)

    # Render template with users and map data
    return render_template('admin_dashboard.html', users=users, user=current_user, map_data=map_data)

    def get_ai_doctor_data(self):
        """
        This function retrieves all AiDoctor entries associated with the user.
        """
        return AiDoctor.query.filter_by(user_id=self.id).all()


# Commented out as it's not used in the provided code
# @admin.route('/get_locations')
# def get_locations():
#     users = User.query.all()  # Get all users
#     locations = []
#     for user in users:
#         locations.append({
#             'username': user.username,
#             'latitude': user.latitude,
#             'longitude': user.longitude,
#             'details': user.first_name # Replace with actual user details
#         })
#     return jsonify(locations)
