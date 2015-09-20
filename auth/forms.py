from wtforms import Form
from wtforms.fields import TextField, PasswordField, HiddenField, SubmitField
from wtforms import validators


class FormWithRedirect(Form):
    redirectTo = HiddenField()


class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    login_button = SubmitField('Login')
