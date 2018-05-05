# python-amcrest-noauth-proxy

[![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](http://www.repostatus.org/badges/latest/concept.svg)](http://www.repostatus.org/#concept)

Python/Flask reverse proxy server that removes HTTP Digest auth from Amcrest IP cameras. Docker image provided.

Developed for Python 3.6, Flask 1.0.2, gunicorn 19.8.1.

This works as a reverse proxy, handling HTTP Digest authentication on the user's behalf (authenticating to the IP camera) and providing (from the user/client perspective) completely unauthenticated access to the camera. I've tested it with the CGI API including snapshots **and mjpeg stream** and it works for all of them. It does _not_ work for the web UI itself or RSTP streams.

mjpeg performance is tolerable but not amazing, with a latency of up to 30 seconds in my tests. However, you should be able to both stream mjpeg and access other CGI commands concurrently.

Note that this proxy only supports one backend camera at a time; even with the gthread threaded worker, performance suffers considerably when I tested multiple camera support. If you have multiple cameras, just run multiple instances of this proxy on different ports.

## Status

This was just a proof-of-concept of mine. I'm not sure if I'm even going to use it myself (at the moment I'm not). Pull requests are welcome, but feature requests aren't likely to result in much.

## Running via Docker

As an example, to expose a camera running at 192.168.0.61 with credentials admin:password on port 8000 of your local machine:

```
docker run -it --rm --name cam-proxy \
    -e CAM_ADDR=192.168.0.61 \
    -e CAM_USER=admin \
    -e CAM_PASS=password \
    -p 8000:8080 jantman/python-amcrest-noauth-proxy
```

Then you should be able to point your browser to, say:

* http://127.0.0.1:8000/cgi-bin/snapshot.cgi
* http://127.0.0.1:8000/cgi-bin/mjpg/video.cgi?channel=1&subtype=1
* http://127.0.0.1:8000/cgi-bin/ptz.cgi?action=start&channel=1&code=Position&arg1=-3000&arg2=0&arg3=0

## Running Locally

Install the requirements in a virtualenv, then:

``gunicorn -c python:gunicorn_config amcrest_noauth_proxy:app``

Note that gunicorn's default "sync" worker type will completely block

## Building

``./docker-build.sh``

## License

python-amcrest-noauth-proxy is licensed under the [GNU Affero General Public License, version 3 or later](https://www.gnu.org/licenses/agpl-3.0.en.html).

What this means to you:

* If you're just running it for personal use, on your own network, with only you accessing it: nothing.
* If you're either distributing this software, or allowing other people to interact with it (i.e. allowing other people or systems to use the proxy or view content that passes through it): everyone who either receives this software _or interacts with it over a network, i.e. sends traffic to or receives traffic from this application_ must be notified that the software is licensed under the AGPL and given access to the source code (i.e. a link to my GitHub repo).
* If you're doing the above _and modifying_ this project, know that users are legally entitled to the exact running source code that they're interacting with. If you modify this, simply linking to my GitHub is not sufficient.
