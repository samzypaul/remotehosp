from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                if user.id == 1:
                    flash('Admin Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))

            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(username=username,latitude=latitude,longitude=longitude,email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


def get_health_news():
    # Replace with your actual API endpoint URL and key
    api_url = 'https://newsapi.org/v2/top-headlines?q=health&apiKey=pub_425134bc3cf1daf5caf290d6026b1cfd78cd2'

    # Consider using environment variables (e.g., `.env`) to store your API key for security
    # response = requests.get(api_url, params={'apiKey': YOUR_API_KEY})

    response = requests.get(api_url)
    data = response.json()

    # Handle potential errors (e.g., API request failure, invalid JSON response)
    if response.status_code == 200:
        articles = data['articles']  # Assuming 'articles' key in the API response
    else:
        articles = []  # Handle error gracefully (e.g., display an error message)

    return render_template('home.html', articles=articles)
@auth.route('/')
def news():
    return redirect('/get_health_news')