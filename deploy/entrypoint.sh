#!/usr/bin/env bash

APP=/app
mkdir -p /data/log

python3 -Wd manage.py makemigrations
python3 manage.py collectstatic --noinput
python3 -Wd manage.py migrate --fake-initial
python3 -Wd manage.py initadmin
exec supervisord