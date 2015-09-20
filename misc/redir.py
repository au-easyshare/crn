from urlparse import urlparse, urljoin
from flask import request, url_for, redirect, g


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target():
    redirs = [request.values.get('next'), request.referrer]
    if hasattr(g, 'default_redir'):
        redirs.append(url_for(g.default_redir))
    for target in redirs:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


#demo
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    next = get_redirect_target()
#    if request.method == 'POST':
#        # login code here
#        return redirect_back('index')
#    return render_template('index.html', next=next)
