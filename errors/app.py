from flask import Blueprint, flash, jsonify, request, redirect, url_for
from flask.ext.login import  current_user

from misc.redir import get_redirect_target

errors = Blueprint('errors', __name__, template_folder='templates')


def common_error(message):
    print "error", message
    flash(message)
    if request.is_xhr:
        return jsonify(result="error", message=message)
    else:
        print "redirect to", get_redirect_target()
        return redirect(get_redirect_target())


def OK(message=None):
    if request.is_xhr:
        return jsonify(result="OK", message=message)
    else:
        return redirect(get_redirect_target())


@errors.record
def errors_init(state):
    app = state.app

    @app.errorhandler(404)
    def error_not_found(e):
        return redirect(url_for('home.home') if current_user.is_authenticated else url_for('auth.login'))
        return common_error(str(e))

    @app.errorhandler(403)
    def error_forbidden(e):
        return common_error(str(e))

    @app.errorhandler(400)
    def error_bad_request(e):
        print "abort 400", str(e)
        return common_error("'%s'." % e.description)

