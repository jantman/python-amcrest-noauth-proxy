#!/bin/bash

version=$(git rev-parse --short HEAD)
build_date=$(date -Iseconds)

docker build --no-cache -t jantman/python-amcrest-noauth-proxy .
