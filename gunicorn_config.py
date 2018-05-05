import os

bind = '0.0.0.0:%s' % os.environ.get('GUNICORN_PORT', 8080)
workers = 4
worker_class = 'gthread'
accesslog = '-'
errorlog = '-'

import gunicorn
gunicorn.SERVER_SOFTWARE = 'github.com/jantman/python-amcrest-noauth-proxy'
