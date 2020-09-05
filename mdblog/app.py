from flask import Flask
from .models import db
from .mod_main.controller import main
from .mod_blog.controller import blog
from .mod_admin.controller import admin


import os #pre configs

flask_app = Flask(__name__)

flask_app.config.from_pyfile("/vagrant/configs/default.py")
flask_app.config.from_pyfile("/vagrant/configs/development.py")

db.init_app(flask_app) ##inicializácia db

flask_app.register_blueprint(main)
flask_app.register_blueprint(blog)
flask_app.register_blueprint(admin)

## CLI COMMAND

def init_db(app):
        with app.app_context():
            db.create_all()
            print("Database inicialized")

            default_user = User(username="admin")
            default_user.set_password("admin")
            db.session.add(default_user)
            db.session.commit()
            print("default user was created")
