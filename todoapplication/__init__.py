# todo_application/__init__.py
import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'

# Bootstrap configuration
Bootstrap(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Database and Migration objects
db = SQLAlchemy(app)
Migrate(app, db)

# Login Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

# Blueprint registration
from todoapplication.core.views import core
from todoapplication.users.views import users
from todoapplication.todo_list.views import todo_posts
from todoapplication.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(todo_posts)
app.register_blueprint(error_pages)
