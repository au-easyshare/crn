from wtforms import Form
from wtforms.fields import TextField, HiddenField


class CrnForm(Form):
    EPS_MERCHANT = HiddenField()
    EPS_PASSWORD = HiddenField()
    EPS_TIMESTAMP = HiddenField()  # is set the same value used to generate the fingerprint
    EPS_TYPE = HiddenField()  # is set the same value used to generate the fingerprint "crn"
    EPS_CRN = HiddenField()  # is set the same value used to generate the fingerprint
    EPS_ACTION = HiddenField()  # is set to one of "addcrn", "editcrn" or "deletecrn"
    EPS_RESULTURL = HiddenField()  # your URL that will handle the transaction result
    EPS_FINGERPRINT = HiddenField()


class CrnAddCCForm(CrnForm):
    EPS_CARDNUMBER = TextField('Card Number')
    EPS_EXPIRYMONTH = TextField('Expiry Month')
    EPS_EXPIRYYEAR = TextField('Expiry Year')
