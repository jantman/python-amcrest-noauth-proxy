# -*- coding: utf-8 -*-

import os
from flask import Flask, Response, stream_with_context, render_template, request
import logging
from copy import deepcopy

import requests
from requests.auth import HTTPDigestAuth

app = Flask(__name__)

CAMS = {
    'cam1': {
        'hostname': 'cam1',
        'user': 'admin',
        'pass': os.environ['CAM_PASSWORD'],
        'rstp_path': '/cam/realmonitor?channel=1&subtype=0&proto=Dahua3',
        'passthru': True,
        'ptz': True
    },
    'cam2': {
        'hostname': 'cam2',
        'user': 'admin',
        'pass': os.environ['CAM_PASSWORD'],
        'rstp_path': '/cam/realmonitor?channel=1&subtype=0&proto=Dahua3',
        'passthru': True,
        'ptz': False
    }
}

@app.route('/')
def index():
    camlist = []
    tmp = []
    for k in sorted(CAMS.keys()):
        tmp.append(deepcopy(CAMS[k]))
        tmp[-1]['name'] = k
        if len(tmp) == 2:
            camlist.append(tmp)
            tmp = []
    return render_template('index.html', camlist=camlist)

@app.route('/<string:camname>/<path:path>')
def cam(camname, path):
    if camname not in CAMS:
        return 'Cam name not found in configuration.', 404
    cam = CAMS[camname]
    if path == 'snapshot':
        path = 'cgi-bin/snapshot.cgi'
    elif path == 'mjpeg':
        path = 'cgi-bin/mjpg/video.cgi?channel=1&subtype=1'
    elif path == 'ptzstatus':
        path = 'cgi-bin/ptz.cgi?action=getStatus&channel=1'
    elif path == 'ptzPosition':
        path = '/cgi-bin/ptz.cgi?action=start&channel=1&code=Position&arg1=%s&arg2=%s&arg3=0' % (request.args.get('x'), request.args.get('y'))
    else:
        if not cam['passthru']:
            return 'Cam does not have passthru configured; unknown path %s' % path, 404
    url = 'http://%s/%s' % (cam['hostname'], path)
    req = requests.get(url, stream = True, auth=HTTPDigestAuth(cam['user'], cam['pass']))
    return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])

if __name__ == '__main__':
    for h in app.logger.handlers:
        h.setLevel(logging.INFO)
    app.run()
