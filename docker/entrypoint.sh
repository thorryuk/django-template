#!/bin/sh

nginx
nohup python manage.py runserver --settings detikconnect_ng.settings.docker_connect 127.0.0.1:8000 > /var/log/connect.log 2>&1 &
nohup python manage.py runserver --settings detikconnect_ng.settings.docker_cms 127.0.0.1:8001 > /var/log/cms.log 2>&1 &
nohup python manage.py runserver --settings detikconnect_ng.settings.docker_worker 127.0.0.1:8002 > /var/log/worker.log 2>&1 &
export DJANGO_SETTINGS_MODULE=detikconnect_ng.settings.docker_worker
celery -A process worker -l info
