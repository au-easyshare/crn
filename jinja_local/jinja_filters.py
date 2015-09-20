import urlparse
from misc.menu import global_menu
from flask import url_for
from cdns import cdns

from wtforms.fields import HiddenField

def init_app(app):
    @app.template_filter('astime')
    def astime(value):
        return value.strftime('%a %d %b %y %I:%M%p')

#    @app.template_filter('csd')
#    def url_basename(value):
#        if not value:
#            return "0"
#        number = int(value) / 1024
#        s = '%d' % number
#        groups = []
#        while s and s[-1].isdigit():
#            groups.append(s[-3:])
#            s = s[:-3]
#        return s + ','.join(reversed(groups))


    @app.template_global('bootstrap_is_hidden_field')
    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)


    @app.template_filter('find_resource')
    def find_resource(ss, version=None):
        if ss not in cdns:
            print "jinja template find_resource failed on", ss
            return "jinja template find_resource failed on", ss
        url = cdns[ss].url(ss, version)
        return url

    app.jinja_env.globals['menu'] = global_menu

