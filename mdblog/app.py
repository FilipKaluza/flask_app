from flask import Flask, render_template
from .database import articles
from flask import g
import sqlite3
from flask import request ##pre login
from flask import redirect ##pre login 
from flask import url_for
from flask import session ## umožnuje prácu s cookies pre indentifikáciu usera

DATABASE = "/vagrant/blog.db"

flask_app = Flask(__name__)
flask_app.secret_key = b'\x1b\n\xc8\xa0\xcf\xd1\xear\x7f\xf3\xeas$\x05\xd1\xf7[!\x17\xd4\xab!p\xda' ##šifra cookies na strane klienta


@flask_app.route('/')
def view_welcome_page():
    return render_template("welcome_page.jinja")

@flask_app.route('/about/')
def view_about():
    return render_template("about.jinja")

@flask_app.route('/admin/')
def view_admin():
    if "logged" not in session: ## ak nie som lognutý
        return redirect(url_for("view_login"))
    return render_template("admin.jinja")

@flask_app.route('/articles/')
def view_articles():
    return render_template("articles.jinja", articles=articles.items())

@flask_app.route('/articles/<int:art_id>/')
def view_article(art_id):
    article = articles.get(art_id)
    if article:
        return render_template("article.jinja", article=article)
    return render_template("article_not_found.jinja", art_id=art_id)

@flask_app.route('/login/', methods=["GET"])
def view_login():
    return render_template("login.jinja")

@flask_app.route('/login/', methods=["POST"])
def login_user():
    username = request.form["username"]
    password = request.form["password"]
    if username == "admin" and password == "admin":
        session["logged"] = True
        return redirect(url_for("view_admin"))
    else:
        return redirect(url_for("view_login"))

@flask_app.route('/logout/', methods=["POST"])
def logout_user():
    session.pop("logged")
    return redirect(url_for("view_welcome_page"))


## UTILS (connect databazy)
def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row ## .Row upraví súrovú db do python dictionary
    return rv

def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@flask_app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlitedb"):
        g.sqlite_db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        with open("mdblog/schema.sql", "r") as fp:
            db.cursor().executescript(fp.read())
        db.commit()

