# DJANGO TEMPLATE

## Installation :
* Run code below :
  * DJANGO_SETTINGS_MODULE=app.settings.cms ./manage.py runserver 0.0.0.0:8000 > /var/log/pln.log 2>&1 &
  * DJANGO_SETTINGS_MODULE=app.settings.frontend ./manage.py runserver 0.0.0.0:8008 > /var/log/pln_frontend.log 2>&1 &
  * DJANGO_SETTINGS_MODULE=app.settings.scheduler /env/bin/python /env/bin/celery -A scheduler worker --beat -l info -E > /var/log/pln_scheduler.log 2>&1 &

## Nginx Configuration :
* Dapat melihat pada file docker/nginx/default_setting.conf
    
## Link Configuration :
* Konfigurasi url link bisa di setting di /pln/context_processor.py

## Database Configuration :
Untuk pengaturan database terdapat di :
* app/settings/, filenya :
    * cms.py
    * frontend.py
    * scheduler.py
