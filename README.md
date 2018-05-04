# python-amcrest-noauth-proxy

Python/Flask reverse proxy server that removes HTTP Digest auth from Amcrest IP cameras. Docker image provided.

Developed for Python 3.6, Flask 1.0.2, gunicorn 19.8.1.

This works as a reverse proxy, handling HTTP Digest authentication on the user's behalf (authenticating to the IP camera) and providing (from the user/client perspective) completely unauthenticated access to the camera. I've tested it with the CGI API, snapshots, _and mjpeg stream_ and it works for all of them.

mjpeg performance is tolerable but not amazing, with a latency of up to 30 seconds in my tests. However, you should be able to both stream mjpeg and access other CGI commands concurrently.

Note that this proxy only supports one backend camera at a time; even with the gthread threaded worker, performance suffers considerably when I tested multiple camera support. If you have multiple cameras, just run multiple instances of this proxy on different ports.

## Running via Docker

As an example, to expose a camera running at 192.168.0.61 with credentials admin:password on port 8000 of your local machine:

```
docker run -it --rm --name cam-proxy -e CAM_ADDR=192.168.0.61 -e CAM_USER=admin -e CAM_PASS=password -p 8000:80 jantman/python-amcrest-noauth-proxy
```

Then you should be able to point your browser to, say:

* http://127.0.0.1:8000/cgi-bin/snapshot.cgi
* http://127.0.0.1:8000/cgi-bin/mjpg/video.cgi?channel=1&subtype=1
* http://127.0.0.1:8000/cgi-bin/ptz.cgi?action=start&channel=1&code=Position&arg1=-3000&arg2=0&arg3=0

## Running Locally

Install the requirements in a virtualenv, then: ``gunicorn -w 4 -b 127.0.0.1:5050 -k gthread --access-logfile - --error-logfile - example:app``

Note that gunicorn's default "sync" worker type will completely block

## Building

``./docker-build.sh``
