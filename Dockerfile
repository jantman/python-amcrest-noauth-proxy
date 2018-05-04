FROM python:3.6.4-alpine3.7

ARG version
ARG build_date

USER root
WORKDIR /app
COPY requirements.txt requirements.txt
COPY amcrest_noauth_proxy.py amcrest_noauth_proxy.py
COPY entrypoint.sh entrypoint.sh
COPY LICENSE LICENSE
COPY README.md README.md
RUN pip install -r requirements.txt && apk add --no-cache tini

ENV LANG=en_US.UTF-8
ENV PYTHONUNBUFFERED=true
LABEL org.label-schema.build-date=$build_date org.label-schema.vcs-url="https://github.com/jantman/python-amcrest-noauth-proxy" org.label-schema.vcs-ref=$version org.label-schema.schema-version="1.0"

EXPOSE 80
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/app/entrypoint.sh"]
