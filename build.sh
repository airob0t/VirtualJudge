#!/bin/sh
docker build -t virtualjudge/virtualjudge .
docker-compose up -d
