from flask import Blueprint, render_template
from flask import render_template, request, redirect, url_for, flash ##pre newsletters
from .forms import NewsletterForm

from mdblog.models import Newsletter ## pre newsletters
from mdblog.models import db ## pre newsletters

import os #pre congigs

main = Blueprint("main", __name__)

## CONTROLLERS
@main.route('/')
def view_welcome_page():
    return render_template("mod_main/welcome_page.jinja")

@main.route('/about/')
def view_about():
    return render_template("mod_main/about.jinja")

@main.route("/newsletter/", methods=["POST"])
def add_newsletter():
    newsletter_form = NewsletterForm(request.form)
    if newsletter_form.validate():
        newsletter = Newsletter(email = newsletter_form.email.data)
        db.session.add(newsletter)
        db.session.commit()
        flash("Great, you were added to subscribers", "success")
    else:
        for error in newsletter_form.errors:
            flash("{} is not valid".format(error), "danger" )
    return redirect(url_for("main.view_welcome_page"))
