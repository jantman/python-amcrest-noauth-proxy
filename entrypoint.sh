#!/bin/sh

[ -z "$CAM_ADDR" ] && { >&2 echo "ERROR: CAM_ADDR environment variable must be set"; exit 1; }
[ -z "$CAM_USER" ] && { >&2 echo "ERROR: CAM_USER environment variable must be set"; exit 1; }
[ -z "$CAM_PASS" ] && { >&2 echo "ERROR: CAM_PASS environment variable must be set"; exit 1; }
 gunicorn -w 4 -b 127.0.0.1:80 -k gthread --access-logfile=- --error-logfile=- --log-file=- amcrest_noauth_proxy:app
