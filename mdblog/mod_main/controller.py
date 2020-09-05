from flask import Blueprint, render_template

import os #pre congigs

main = Blueprint("main", __name__)

## CONTROLLERS
@main.route('/')
def view_welcome_page():
    return render_template("mod_main/welcome_page.jinja")

@main.route('/about/')
def view_about():
    return render_template("mod_main/about.jinja")
