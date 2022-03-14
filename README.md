# DJANGO TEMPLATE

## Installation :
* Run code below :
  * DJANGO_SETTINGS_MODULE=pln.settings.cms_docker ./manage.py runserver 0.0.0.0:8000 > /var/log/pln.log 2>&1 &
  * DJANGO_SETTINGS_MODULE=pln.settings.frontend_docker ./manage.py runserver 0.0.0.0:8008 > /var/log/pln_frontend.log 2>&1 &
  * DJANGO_SETTINGS_MODULE=pln.settings.scheduler_docker /env/bin/python /env/bin/celery -A scheduler worker --beat -l info -E > /var/log/pln_scheduler.log 2>&1 &

## Nginx Configuration :
* Dapat melihat pada file docker/nginx/default_setting.conf
    
## Link Configuration :
* Konfigurasi url link bisa di setting di /pln/context_processor.py

## Database Configuration :
Untuk pengaturan database terdapat di :
* pln/settings/, filenya :
    * cms_docker.py
    * frontend_docker.py
    * scheduler_docker.py
