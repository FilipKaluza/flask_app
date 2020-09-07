from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms import HiddenField ## je to potrebné pre markdown editor
from wtforms.validators import InputRequired


## FORMS
class loginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content")
    html_render = HiddenField()

class changePasswordForm(FlaskForm):
    old_password = StringField("Old_assword", validators=[InputRequired()])
    new_password = PasswordField("New_Password", validators=[InputRequired()])
