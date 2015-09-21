#!/usr/bin/env python
import sys
from flask import Flask, g, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ConfigParser
import optparse

import jinja_local.jinja_filters

import auth
import home
import crn
#import errors

import misc

from es_sqla.dbase import adjust_schemas

config_defaults = {'staging_schema': 'staging', 'model_schema': 'easyshare'}


def create_app(options):
    app = Flask(__name__)

    app.secret_key = 'ed788cab1d449175885623bf5fad28101898b059380a263f'

    config = ConfigParser.ConfigParser()
    config.readfp(open(options.config))

    app.mopts = misc.MagicOptions(config_defaults, dict(config.items(options.section)), vars(options), dict(section=options.section))
    app.users = dict(config.items('users_' + options.section))
    engine = create_engine(app.mopts.uri)
    adjust_schemas(staging=app.mopts.staging_schema, model=app.mopts.model_schema)
    Session = sessionmaker(bind=engine)  # autocommit=True)

    auth.init_login_manager(app)
    jinja_local.jinja_filters.init_app(app)
    misc.menu.init_app(app)

    app.register_blueprint(auth.auth)
#    app.register_blueprint(errors.errors)
    app.register_blueprint(home.homebp, url_prefix='/home')
    app.register_blueprint(crn.crnbp, url_prefix='/crn')

#    @app.route('/')
#    def root():
#        return redirect(url_for('binterface.ctl_jobs', filter='php_only'))

    @app.after_request
    def session_commit(response):
        session = getattr(g, 'session', None)
        if session is not None:
            g.session.commit()
        return response

    @app.before_request
    def before_request():
        g.session = Session()

    @app.teardown_request
    def teardown_request(exception):
        session = getattr(g, 'session', None)
        if session is not None:
            session.close()
    return app


def load_app(section):
    class options:
        def __init__(self, section):
            self.section = section
            self.config = 'settings.ini'
            self.echo = False
    return create_app(options(section))


if __name__ == '__main__':
    if sys.platform == 'darwin':
        host = 'localhost'
    else:
        host = '0.0.0.0'

    parser = optparse.OptionParser()
    parser.add_option("-f", "--config", dest="config", default='settings.ini', help="config file")
    parser.add_option("-s", "--section", dest="section", default='beta', help="config file section")
    parser.add_option("-e", "--echo", dest="echo", action="store_true", default=False, help="echo sql")
    parser.add_option("-p", "--port", dest="port", default=8080, type="int", help="Set listeding port")
    options, args = parser.parse_args()
    app = create_app(options)
    app.run(debug=True, port=options.port, host=host)
