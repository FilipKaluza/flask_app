from flask import Flask, render_template
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
flask_app.register_blueprint(admin, url_prefix="/admin") ## všetko podurl bude za /admin


## ERROR handler
@flask_app.errorhandler(500)
def Internal_server_error(error):
    return render_template("errors/500.jinja"), 500

@flask_app.errorhandler(404)
def Internal_server_error(error):
    return render_template("errors/404.jinja"), 404



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
