#!/usr/bin/env python

#
# This file may be used instead of Apache mod_wsgi to run your python
# web application in a different framework.  A few examples are
# provided (cherrypi, gevent), but this file may be altered to run
# whatever framework is desired - or a completely customized service.
#

import tornado.ioloop
import main
import os

try:
    zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'], 'virtenv',
                            'bin', 'activate_this.py')
    execfile(zvirtenv, dict(__file__=zvirtenv))
except IOError:
    pass

if __name__ == '__main__':
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
    app = main.MainAPI()

    app.application.listen(port, ip)
    tornado.ioloop.IOLoop.current().start()
