import logging

from celery import Celery
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template import Context
from django.template.loader import get_template

from app.common_functions import password_generator


LOG = logging.getLogger(__name__)

def show_forget_password(request):

    data = {'title': 'PPA | E-Reqruitment System - Forgot Password',
            'sub_title': 'PPA | E-Reqruitment System'}

    return render(request, 'pln/backend/forget_password.html', data)


def do_reset_password(request):

    default_response = redirect('forget_password')
    if request.method == 'POST':

        try:
            user = User.objects.get(email=request.POST.get('email'))

            default_password = password_generator()
            user.set_password(default_password)
            user.save()
        except User.DoesNotExist:
            default_response.set_cookie('error_msg', 'user not found', max_age=2)
            return default_response

        # Send Email Success Activation
        host = settings.BACKEND_HOST_PROTOCOL + '://' + request.META['HTTP_HOST']
        email_template = get_template('pln/email/success_reset_password_user.html')
        email_template_param = {'username': user.email, 'password': default_password,
                                        'host': host}
        email_template_render = email_template.render(email_template_param)

        send_mail_parameters = {
            'to': [user.email],
            'from': 'Nippon Express <' + settings.DEFAULT_MAIL_FROM + '>',
            'subject': 'Anda Sukses Melakukan Reset Password',
            'html': email_template_render
        }

        try:
            celery = Celery()
            celery.config_from_object('django.conf:settings', namespace='CELERY')
            celery.send_task("scheduler.tasks.send_mail_task", args=[send_mail_parameters],
                             queue='celery', routing_key='celery')
        except Exception as exception:
            LOG.error(exception)

        return render(request, 'pln/backend/success_forget_password.html', None)

    default_response.set_cookie('error_msg', 'invalid method type', max_age=2)
    return default_response