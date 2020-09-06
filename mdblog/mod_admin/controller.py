from flask import Blueprint, render_template

from flask import request ##pre login
from flask import redirect ##pre login 
from flask import url_for
from flask import session ## umožnuje prácu s cookies pre indentifikáciu usera
from flask import flash

## pre DB
from mdblog.models import db
from mdblog.models import Article 
from mdblog.models import User

admin = Blueprint("admin", __name__)

## FORMS
from .forms import ArticleForm, loginForm, changePasswordForm

##for @login_required 
from functools import wraps
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "logged" not in session:
            flash("You must be logged in", "alert-danger")
            return redirect(url_for("admin.view_login"))
        return func(*args, **kwargs)
    return decorated_function

## Adminpage
@admin.route('/')
@login_required
def view_admin():
    page=request.args.get("page", 1, type=int)
    paginate = Article.query.order_by(Article.id.desc()).paginate(
            page, 3, False)
    return render_template("mod_admin/admin.jinja",
            articles=paginate.items, 
            paginate=paginate)

@admin.route('/articles/new/', methods=["GET"])
@login_required
def view_add_article():
    form = ArticleForm()
    return render_template("mod_admin/article_editor.jinja", form=form)


## s metódou POST na pridanie článku
@admin.route('/articles/', methods=["POST"])
@login_required
def add_article():
    add_form = ArticleForm(request.form)
    if add_form.validate():
        new_article = Article(
            title = add_form.title.data,
            content = add_form.content.data)
        db.session.add(new_article)
        db.session.commit()
        flash(u"Article was added", category="alert-success")
        return redirect(url_for("blog.view_articles"))

## editácia article
@admin.route('/articles/<int:art_id>/edit/', methods=["GET"])
@login_required
def view_article_editor(art_id):
    article = Article.query.filter_by(id = art_id).first()
    if article:
        form = articleForm()
        form.title.data = article.title
        form.content.data = article.content
        return render_template("article_editor.jinja", form=form, article=article)
    return render_template("mod_blog/article_not_found.jinja", art_id=art_id)


@admin.route('/articles/<int:art_id>/', methods=["POST"])
@login_required
def edit_article(art_id):
    article = Article.query.filter_by(id = art_id).first()
    if article:
        edit_form = articleForm(request.form)
        if edit_form.validate():
            article.title = edit_form.title.data
            article.content = edit_form.content.data
            db.session.add(article)
            db.session.commit()
            flash("Changes was saved", "success")
            return redirect(url_for("admin.view_article", art_id=art_id))


## CHANGE PASSWORD
@admin.route("/changepassword/", methods=["GET"])
@login_required
def view_change_password():
    form = changePasswordForm()
    return render_template("mod_admin/change_password.jinja", form=form)

@admin.route("/changepassword/", methods=["POST"])
@login_required
def change_password():
    form = changePasswordForm(request.form)
    if form.validate():
        user = User.query.filter_by(username = session["logged"]).first()
        if user and user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db.session.add(user)
            db.session.commit()
            flash("Password was changed", category="success")
            return redirect(url_for("admin.view_admin"))


@admin.route('/login/', methods=["GET"])
def view_login():
    login_form = loginForm()
    return render_template("mod_admin/login.jinja", form=login_form)

##LOG IN
@admin.route('/login/', methods=["POST"])
def login_user():
    login_form = loginForm(request.form) ## inštancia formuláru loginForm
    if login_form.validate(): ##ak sú obe polia vyplnené
        user = User.query.filter_by(username = login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            session["logged"] = user.username
            flash("Login succesfull", category="success")
            return redirect(url_for("admin.view_admin"))
        else:
            flash("Invalid username or password", category="danger")
            return redirect(url_for("admin.view_login"))
    else:
        for error in login_form.errors:
            flash("{} is missing".format(error), "danger")
        return redirect(url_for("admin.view_login"))


##LOGOUT
@admin.route('/logout/', methods=["POST"])
def logout_user():
    session.pop("logged")
    flash(u"You had been logged out", category="success")
    return redirect(url_for("main.view_welcome_page"))

