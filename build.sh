#!/bin/bash

docker build . -t ghcr.io/samsimpson1/starling-notify:latest
docker push ghcr.io/samsimpson1/starling-notify:latest