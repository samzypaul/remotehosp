from flask import Flask,g
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_admin import Admin
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user

db = SQLAlchemy()
DB_NAME = "database.db"

#'mysql+pymysql://username:password@localhost/db_name'
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin import admin
    from .prediction import pred

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(pred, url_prefix='/')

    from .models import User, Note, AiDoctor
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @app.before_request
    def before_request():
        g.user = current_user

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

# def create_admin(app):
#     from app import db, User, Role
#     from werkzeug.security import generate_password_hash
#
#     admin_user = User(username='admin', email='admin@example.com',
#                       password_hash=generate_password_hash('admin_password'),
#                       role=Role.ADMIN)
#     db.session.add(admin_user)
#     db.session.commit()


# def admin_acc(app):
#     from .models import MyModelView
#     admin = Admin(create_app())
#     admin.add_view(MyModelView(current_user,db.session))