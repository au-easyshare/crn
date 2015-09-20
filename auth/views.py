import time
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask.ext.login import LoginManager, login_required, login_user, logout_user, UserMixin, current_app

import forms

auth = Blueprint('auth', __name__, template_folder='templates')


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        supers = current_app.mopts.supers.split(',')
        self.is_super = True if id in supers else False


def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(userid):
        return User(userid)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            if form.username.data in current_app.users and form.password.data == current_app.users[form.username.data]:
                login_user(User(form.username.data))
                return redirect(request.args.get('next') or url_for('home.home'))
            else:
                flash("Bad login")
                time.sleep(3)
        else:
            for field, issue in form.errors.items():
                flash("field '%s' has an issue '%s'" % (field, ' '.join(issue)), category='danger')
    return render_template('login.html', form=form)
