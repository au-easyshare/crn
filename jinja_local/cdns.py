import flask
import os
import sys
import urlparse
import urllib2
import argparse

from flask import url_for

use_min = False
local_only = False

class CDNSpec():
    def __init__(self, urlBase, version=None, hasMin=True):
        self.urlBase = urlBase
        self.hasMin = hasMin
        self.version = version

    def url(self, file_name, version=None):
        if not version:
            version = self.version
        if use_min and self.hasMin:
            file_basename, extension = os.path.splitext(file_name)
            if extension == '.js':
                file_name = file_basename + '.min' + extension

        url = os.path.join(self.urlBase, file_name)
        oo = urlparse.urlparse(url)
        if oo.scheme == 'file':
            url = url_for('static', filename=oo.path[1:])
        elif local_only:
            url = url_for('static', filename=os.path.join('cache', file_name))

        return url.format(version=version or '')


# note that file: schema items have 3 / because the netloc is empty
cdns = {'jquery.js': CDNSpec('//ajax.googleapis.com/ajax/libs/jquery/{version}/', version='1.11.2'),
        'jquery-ui.js': CDNSpec('//cdnjs.cloudflare.com/ajax/libs/jqueryui/{version}/', version='1.11.2'),

        'bootstrap.js': CDNSpec('//netdna.bootstrapcdn.com/bootstrap/{version}/js/', version='3.3.2'),
        'bootstrap.css': CDNSpec('//netdna.bootstrapcdn.com/bootstrap/{version}/css/', version='3.3.2'),

        'jquery.dataTables.js': CDNSpec('//cdn.datatables.net/{version}/js', version='1.10.7'),
        'jquery.dataTables.css': CDNSpec('//cdn.datatables.net/{version}/css', version='1.10.7'),
        'dataTables.bootstrap.js': CDNSpec('//cdn.datatables.net/plug-ins/{version}/integration/bootstrap/3/', version='1.10.7'),
        'dataTables.bootstrap.css': CDNSpec('//cdn.datatables.net/plug-ins/{version}/integration/bootstrap/3/', version='1.10.7'),

        'dataTables.responsive.js': CDNSpec('//cdn.datatables.net/responsive/{version}/js', version='1.0.4'),
        'dataTables.responsive.css': CDNSpec('//cdn.datatables.net/responsive/{version}/css', version='1.0.4'),

        'dataTables.fixedColumns.js': CDNSpec('//cdn.datatables.net/fixedcolumns/{version}/js', version='3.0.4'),
        'dataTables.fixedColumns.css': CDNSpec('//cdn.datatables.net/fixedcolumns/{version}/css', version='3.0.4'),

        'moment.js': CDNSpec('//cdnjs.cloudflare.com/ajax/libs/moment.js/{version}/', version='2.10.3'),
#        'date.min.js': CDNSpec('//cdnjs.cloudflare.com/ajax/libs/datejs/{version}/', version='1.0', hasMin=False),

        # local yokel
#        'dataTables.local.css': CDNSpec('file:///css/', hasMin=False),
        'dtables.js': CDNSpec('file:///js/', hasMin=False),
        'bootstrap-submenu.js': CDNSpec('//cdn.easyshare.money/bootstrap-submenu/dist/js/'),
        'bootstrap-submenu.css': CDNSpec('//cdn.easyshare.money/bootstrap-submenu/dist/css/')
#        'asmet-likes.js': CDNSpec('file:///js/', hasMin=False),
#        'url_action.js': CDNSpec('file:///js/', hasMin=False),
#        'lmap.js': CDNSpec('file:///js/', hasMin=False)

}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    args = parser.parse_args()


    def test_schemed(url):
        if url[:2] == '//':
            return "http:" + url, 'http'
        elif url[0] == '/':
            return "file:/" + url, 'file'
        else:
            print "unknown scheme on", url
            sys.exit(1)
    agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', agent)]
    app = flask.Flask('__name__')
    with app.test_request_context():
        for file_key in cdns.keys():
            url = cdns[file_key].url(file_key)
            qo, scheme = test_schemed(url)
            if scheme == 'http':
                try:
                    response = opener.open(qo)
                except Exception as e:
                    print "error", e, "on ", file_key, "as", url, "tried", qo
                else:
                    print "OK found", file_key
                if args.file:
                    path = os.path.join(args.file, file_key)
                    ff = open(path, 'w')
                    ff.write(response.read())
                    ff.close()
            elif scheme == 'file':
                uparsed = urlparse.urlparse(qo)
                fpath = uparsed.netloc + uparsed.path
                if not os.path.isfile(fpath):
                    print "error", file_key, "as", url, "tried", fpath
                else:
                    print "OK found file", file_key
            


#<link href="css/plugins/morris/morris-0.4.3.min.css" rel="stylesheet">
#<link href="css/plugins/timeline/timeline.css" rel="stylesheet">
#    <script src="js/plugins/metisMenu/jquery.metisMenu.js"></script>
#    <script src="js/plugins/morris/raphael-2.1.0.min.js"></script>
#    <script src="js/plugins/morris/morris.js"></script>
