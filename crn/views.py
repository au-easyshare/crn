import datetime
import base64
import urllib

import requests

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, abort
from flask.ext.login import login_required

from misc.menu import add_menu

import forms

crnbp = Blueprint('crn', __name__, template_folder='templates')


class NABCustMgmt:
    def __init__(self):
        self.base_params = {'EPS_MERCHANT': current_app.mopts.eps_merchant,
                            'EPS_PASSWORD': current_app.mopts.eps_password,
                            'EPS_TYPE': 'CRN'}

    @staticmethod
    def timestamp():
        return datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')

    def signature(self, timestamp, action, crn):
        odict = self.base_params.copy()
        odict['EPS_TIMESTAMP'] = timestamp
        odict['EPS_ACTION'] = action
        odict['EPS_CRN'] = crn
        odict['EPS_ALLOCATEDVARIABLE'] = "1234"
        try:
            print "fprinter", current_app.mopts.fingerprinter
            print "params", odict
            rr = requests.post(current_app.mopts.fingerprinter, params=odict)
        except Exception as ee:
            print "Exception in post", str(ee)
            return None
        result = rr.content
        try:
            pp = base64.b64decode(result)
        except TypeError:
            print "Bad base64"
            abort(404, "type error for signature")
        if pp is None:
            print "Failed to get signature"
            abort(404, "Failed to get signature")
        return result


@add_menu('CRN', 'Request signature', 'requestsig', crnbp)
@crnbp.route('/requestsig')
@login_required
def requestsig():
    cmo = NABCustMgmt()
    timestamp = cmo.timestamp()
    return render_template('cmtest.html', results=dict(signature=cmo.signature(timestamp=timestamp, action="ADDCRN", crn="John Citizen")))


def crn_form(form, timestamp, action, fingerprint, crn):
    return form(request.form,
                EPS_MERCHANT=current_app.mopts.eps_merchant,
                EPS_PASSWORD=current_app.mopts.eps_password,
                EPS_TYPE='CRN',
                EPS_TIMESTAMP=timestamp,
                EPS_ACTION=action,
                EPS_RESULTURL=current_app.mopts.eps_resulturl,
                EPS_FINGERPRINT=urllib.quote_plus(fingerprint),
                EPS_CRN=crn)


@add_menu('CRN', 'enter CC', 'entercc', crnbp)
@crnbp.route('/entercc', methods=['GET', 'POST'])
@login_required
def entercc():
    if request.method == 'POST':
        abort(404, "Got post, not meant to")
    else:
        cmo = NABCustMgmt()
        timestamp = cmo.timestamp()
        crn = "John Citizen"
        action = 'addcrn'
        fingerprint = cmo.signature(timestamp=timestamp, action=action, crn="John Citizen")
        print "Fingerprint is", fingerprint
        addcc_form = crn_form(forms.CrnAddCCForm, timestamp, action, fingerprint, crn="John Citizen")
    return render_template('entercc.html', eps_post=current_app.mopts.eps_post, form=addcc_form)


@crnbp.route('/acceptcc', methods=['POST'])
@login_required
def acceptcc():
    from IPython import embed; embed()
    return "<html>HELLO WORLD</html>"
