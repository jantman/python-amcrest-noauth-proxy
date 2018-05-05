# -*- coding: utf-8 -*-
"""
The latest version of this package is available at:
<http://github.com/jantman/python-amcrest-noauth-proxy>

################################################################################
Copyright 2018 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of python-amcrest-noauth-proxy, also known as
    amcrest-noauth-proxy.

    python-amcrest-noauth-proxy is free software: you can redistribute it and/or
    modify it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the License,
    or (at your option) any later version.

    python-amcrest-noauth-proxy is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with python-amcrest-noauth-proxy.  If not, see
    <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at
<https://github.com/jantman/python-amcrest-noauth-proxy> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
"""

import os
from flask import Flask, Response, stream_with_context, request
import logging

import requests
from requests.auth import HTTPDigestAuth

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def cam(path):
    url = 'http://%s%s' % (os.environ['CAM_ADDR'], request.full_path)
    req = requests.get(
        url,
        stream = True,
        auth=HTTPDigestAuth(os.environ['CAM_USER'], os.environ['CAM_PASS'])
    )
    return Response(
        stream_with_context(req.iter_content()),
        content_type = req.headers['content-type'],
        headers=dict(req.headers).update({
            # Per the terms of the AGPL, these following headers MAY NOT
            # be removed! They MUST be returned to the client.
            'X-Powered-By': 'github.com/jantman/python-amcrest-noauth-proxy',
            'X-License': 'GNU Affero General Public License v3 or later'
        })
    )

if __name__ == '__main__':
    for h in app.logger.handlers:
        h.setLevel(logging.INFO)
    app.run()
