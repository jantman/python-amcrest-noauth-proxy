# python-amcrest-noauth-proxy

Python/Flask reverse proxy server that removes HTTP Digest auth from Amcrest IP cameras.

Developed for Python 3.6 and Flask 1.0.2

Running: ``gunicorn -w 4 -b 127.0.0.1:5050 -k gthread --access-logfile - --error-logfile - example:app``
