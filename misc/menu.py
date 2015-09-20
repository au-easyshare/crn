from flask import safe_join
from functools import wraps
import os

from OrderedDefaultdict import OrderedDefaultdict

global_menu = OrderedDefaultdict(OrderedDefaultdict)

def init_app(app):
    @app.template_global('issubmenu')
    def issubmenu(value):
        # print "is", isinstance(value, OrderedDefaultdict), "type", type(value), "val", value
        return isinstance(value, OrderedDefaultdict)

def add_menu(row_text, col_text, route, blueprint=None, submenu=None):
    if blueprint:
        route = os.path.join('/', safe_join(blueprint.name, route))
    if submenu:
        print "submenu", submenu
        if row_text in global_menu and col_text in global_menu[row_text]:
            if not isinstance(global_menu[row_text][col_text], OrderedDefaultdict):
                print "not ordered dict"
            else:
                print "present and instance added", submenu, "route ", route
                global_menu[row_text][col_text][submenu] = route
        else:
            print "added", submenu, "route", route
            global_menu[row_text][col_text] = OrderedDefaultdict(str)
            global_menu[row_text][col_text][submenu] = route
    else:
        global_menu[row_text][col_text] = route

    @wraps
    def deco(f):
        return f
    return deco
