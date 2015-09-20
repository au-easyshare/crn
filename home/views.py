from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask.ext.login import login_required

homebp = Blueprint('home', __name__, template_folder='templates')


@homebp.route('/home')
@login_required
def home():
    return render_template('home.html', items=dict(users=10))
