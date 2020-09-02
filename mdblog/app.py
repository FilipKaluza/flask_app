from flask import Flask, render_template
from flask import g

from flask import request ##pre login
from flask import redirect ##pre login 
from flask import url_for
from flask import session ## umožnuje prácu s cookies pre indentifikáciu usera
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms.validators import InputRequired

import sqlite3
import os #pre congigs

flask_app = Flask(__name__)

flask_app.config.from_pyfile("/vagrant/configs/default.py")

if "MDBLOG_CONFIG" in os.environ:
    flask_app.config.from_envvar("MDBLOG_CONFIG")

## FORMS
class loginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class articleForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content")

## CONTROLLERS
@flask_app.route('/')
def view_welcome_page():
    return render_template("welcome_page.jinja")

@flask_app.route('/about/')
def view_about():
    return render_template("about.jinja")

## Adminpage
@flask_app.route('/admin/')
def view_admin():
    if "logged" not in session: ## ak nie som lognutý
        flash(u"You must be logged in", "danger")
        return redirect(url_for("view_login"))
    return render_template("admin.jinja")

## ARTICLES ##

## s metódou GET na čítanie článkov
@flask_app.route('/articles/', methods=["GET"])
def view_articles():
    db = get_db()
    cur = db.execute("select * from articles order by id desc") ##cur = cursor
    articles = cur.fetchall()
    return render_template("articles.jinja", articles=articles)

@flask_app.route('/articles/new/', methods=["GET"])
def view_add_article():
    if "logged" not in session:
        return redirect(url_for("view_login"))
    form = articleForm()
    return render_template("article_editor.jinja", form=form)



## s metódou POST na pridanie článku
@flask_app.route('/articles/', methods=["POST"])
def add_article():
    if "logged" not in session:
        return redirect(url_for("view_login"))
    db = get_db()
    db.execute("insert into articles (title, content) values (?, ?)", [request.form.get("title"), request.form.get("content")])
    db.commit()
    flash(u"Article was added", category="alert-success")
    return redirect(url_for("view_articles"))

##Zobrazenie article
@flask_app.route('/articles/<int:art_id>/')
def view_article(art_id):
    db = get_db()
    cur = db.execute("select * from articles where id=(?)",[art_id])
    article = cur.fetchone() ##iba 1 článok
    if article:
        return render_template("article.jinja", article=article)
    return render_template("article_not_found.jinja", art_id=art_id)

## editácia article
@flask_app.route('/articles/<int:art_id>/edit/', methods=["GET"])
def view_article_editor(art_id):
    if "logged" not in session:
        return redirect(url_for("view_login"))
    db = get_db()
    cur = db.execute("select * from articles where id=(?)",[art_id])
    article = cur.fetchone()
    if article:
        form = articleForm()
        form.title.data = article["title"]
        form.content.data = article["content"]
        return render_template("article_editor.jinja", form=form, article=article)
    return render_template("article_not_found.jinja", art_id=art_id)

@flask_app.route('/articles/<int:art_id>/', methods=["POST"])
def edit_article(art_id):
    if "logged" not in session:
        return redirect(url_for("view_login"))
    db = get_db()
    cur = db.execute("select * from articles where id=(?)",[art_id])
    article = cur.fetchone()
    if article:
        edit_form = articleForm(request.form)
        if edit_form.validate():
            db.execute("update articles set title=?, content=? where id=?", [edit_form.title.data, edit_form.content.data, art_id])
            db.commit()
            flash("Changes was saved", "success")
            return redirect(url_for("view_article", art_id=art_id))

@flask_app.route('/login/', methods=["GET"])
def view_login():
    login_form = loginForm()
    return render_template("login.jinja", form=login_form)

##LOG IN
@flask_app.route('/login/', methods=["POST"])
def login_user():
    login_form = loginForm(request.form) ## inštancia formuláru loginForm
    if login_form.validate(): ##ak sú obe polia vyplnené
        if login_form.username.data == flask_app.config["USERNAME"] and login_form.password.data == flask_app.config["PASSWORD"]:
            session["logged"] = True
            flash("Login succesfull", category="success")
            return redirect(url_for("view_admin"))
        else:
            flash("Invalid username or password", category="danger")
            return redirect(url_for("view_login"))
    else:
        for error in login_form.errors:
            flash("{} is missing".format(error), "danger")
        return redirect(url_for("view_login"))

##LOGOUT
@flask_app.route('/logout/', methods=["POST"])
def logout_user():
    session.pop("logged")
    flash(u"You had been logged out", category="success")
    return redirect(url_for("view_welcome_page"))


## UTILS (connect databazy)
def connect_db():
    rv = sqlite3.connect(flask_app.config["DATABASE"])
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

