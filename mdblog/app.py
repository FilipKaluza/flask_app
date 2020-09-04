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

## pre DB
from .models import db
from .models import Article 
from .models import User


import os #pre congigs

flask_app = Flask(__name__)

flask_app.config.from_pyfile("/vagrant/configs/default.py")
flask_app.config.from_pyfile("/vagrant/configs/development.py")

db.init_app(flask_app) ##inicializácia db

## FORMS
class loginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class articleForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content")

class changePasswordForm(FlaskForm):
    old_password = StringField("Old_assword", validators=[InputRequired()])
    new_password = PasswordField("New_Password", validators=[InputRequired()])


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
    articles = Article.query.order_by(Article.id.desc())
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
    add_form = ArticleForm(request.form)
    if add_form.validate():
        new_article = Article(
            title = add_form.title.data,
            content = add_form.content.data)
        db.session.add(new_article)
        db.session.commit()
        flash(u"Article was added", category="alert-success")
        return redirect(url_for("view_articles"))

##Zobrazenie article
@flask_app.route('/articles/<int:art_id>/')
def view_article(art_id):
    article = Article.query.filter_by(id=art_id).first()
    if article:
        return render_template("article.jinja", article=article)
    return render_template("article_not_found.jinja", art_id=art_id)

## editácia article
@flask_app.route('/articles/<int:art_id>/edit/', methods=["GET"])
def view_article_editor(art_id):
    if "logged" not in session:
        return redirect(url_for("view_login"))
    article = Article.query.filter_by(id = art_id).first()
    if article:
        form = articleForm()
        form.title.data = article.title
        form.content.data = article.content
        return render_template("article_editor.jinja", form=form, article=article)
    return render_template("article_not_found.jinja", art_id=art_id)

@flask_app.route('/articles/<int:art_id>/', methods=["POST"])
def edit_article(art_id):
    if "logged" not in session:
        return redirect(url_for("view_login"))
    article = Article.query.filter_by(id = art_id).first()
    if article:
        edit_form = articleForm(request.form)
        if edit_form.validate():
            article.title = edit_form.title.data
            article.content = edit_form.content.data
            db.session.add(article)
            db.session.commit()
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
        user = User.query.filter_by(username = login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            session["logged"] = user.username
            flash("Login succesfull", category="success")
            return redirect(url_for("view_admin"))
        else:
            flash("Invalid username or password", category="danger")
            return redirect(url_for("view_login"))
    else:
        for error in login_form.errors:
            flash("{} is missing".format(error), "danger")
        return redirect(url_for("view_login"))

## CHANGE PASSWORD
@flask_app.route("/changepassword/", methods=["GET"])
def view_change_password():
    if "logged" not in session:
        return redirect(url_for("view_login"))
    form = changePasswordForm()
    return render_template("change_password.jinja", form=form)

@flask_app.route("/changepassword/", methods=["POST"])
def change_password():
    if "logged" not in session:
        return redirect(url_for("view_login"))
    form = changePasswordForm(request.form)
    if form.validate():
        user = User.query.filter_by(username = session["logged"]).first()
        if user and user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db.session.add(user)
            db.session.commit()
            flash("Password was changed", category="success")
            return redirect(url_for("view_admin"))


##LOGOUT
@flask_app.route('/logout/', methods=["POST"])
def logout_user():
    session.pop("logged")
    flash(u"You had been logged out", category="success")
    return redirect(url_for("view_welcome_page"))


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
