# -*- coding: utf-8 -*-

import os
from flask import Flask, Response, stream_with_context, request
import logging

import requests
from requests.auth import HTTPDigestAuth

app = Flask(__name__)

@app.route('/<path:path>')
def cam(path):
    url = 'http://%s/%s' % (os.environ['CAM_ADDR'], path)
    req = requests.get(
        url,
        stream = True,
        auth=HTTPDigestAuth(os.environ['CAM_USER'], os.environ['CAM_PASS'])
    )
    return Response(
        stream_with_context(req.iter_content()),
        content_type = req.headers['content-type']
    )

if __name__ == '__main__':
    for h in app.logger.handlers:
        h.setLevel(logging.INFO)
    app.run()
