################################################################################
# The latest version of this package is available at:
# <http://github.com/jantman/python-amcrest-noauth-proxy>
#
################################################################################
# Copyright 2018 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
#
#    This file is part of python-amcrest-noauth-proxy, also known as
#    amcrest-noauth-proxy.
#
#    python-amcrest-noauth-proxy is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the License,
#    or (at your option) any later version.
#
#    python-amcrest-noauth-proxy is distributed in the hope that it will be
#    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with python-amcrest-noauth-proxy.  If not, see
#    <http://www.gnu.org/licenses/>.
#
# The Copyright and Authors attributions contained herein may not be removed or
# otherwise altered, except to add the Author attribution of a contributor to
# this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
# While not legally required, I sincerely request that anyone who finds
# bugs please submit them at
# <https://github.com/jantman/python-amcrest-noauth-proxy> or
# to me via email, and that you send any contributions or improvements
# either as a pull request on GitHub, or to me via email.
################################################################################
#
# AUTHORS:
# Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################

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

USER nobody
EXPOSE 8080
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/app/entrypoint.sh"]
