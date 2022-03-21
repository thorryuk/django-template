from calendar import HTMLCalendar
import datetime
import hashlib
import logging
from os import urandom
import random

from celery import Celery
from dateutil.relativedelta import relativedelta
from django import http
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect, HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse
from django.utils.timezone import now

from backend.forms import AddUserForm, EditUserForm
from backend.models import UserExtend, RoleUser, RoleGroup
from app.common_functions import handle_uploaded_file_local, password_generator, uploads


LOG = logging.getLogger(__name__)


def show_user_list(request):
    data = {
        'title': settings.GLOBAL_TITLE + ' | User List',
        'sub_title': 'User List',
        'profile_pict': '',
        'email': '',
        'name': '',
        'active_menu': 'admin',
        'sub_menu': 'admin_user'
    }

    user_list = User.objects.filter(is_staff=1, is_superuser=0, admin_user__is_deleted=False).order_by('first_name')
    paginator = Paginator(user_list, 12)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    data['users'] = users

    return render(request, 'backend/user-management/list.html', data)


def add_new_user(request):

    data = {
        'title': settings.GLOBAL_TITLE + ' | Add New User',
        'sub_title': 'Add New User',
        'profile_pict': '',
        'email': '',
        'name': '',
        'active_menu': 'admin',
        'sub_menu': 'admin_user',
        'form': AddUserForm(),
        'roles': RoleGroup.objects.filter()
    }

    if request.method == 'POST':
        data['form'] = AddUserForm(request.POST, request.FILES)
        form = data['form']

        if form.is_valid():

            cleaned_data = form.clean()

            first_name = str(cleaned_data.get('first_name')).lower()
            last_name = str(cleaned_data.get('last_name')).lower()
            email = str(cleaned_data.get('email')).lower()
            gender = cleaned_data.get('gender')
            address = str(cleaned_data.get('address'))
            # phone = str(cleaned_data.get('phone')).lower()
            # email_signature = str(cleaned_data.get('email_signature')).lower()
            roles = cleaned_data.get('roles')

            # validate email user
            user_by_email = User.objects.filter(email=email)
            if len(user_by_email) > 0:
                response = redirect(reverse('user_list'))
                response.set_cookie('error_msg', 'User already exists', max_age=2)
                return response

            profile_pict = ''
            if 'images' in request.FILES:
                profile_pict = uploads('profile-pictures', request.FILES['images'])

            # start transaction
            sid = transaction.savepoint()

            activation_key = generate_act_key(email)

            try:
                default_password = password_generator()

                # create django user
                insert_user = User(username=email,
                                   email=email,
                                   first_name=first_name,
                                   last_name=last_name,
                                   is_active=True,
                                   is_staff=True,
                                   password=make_password(default_password))
                insert_user.save()


                today = datetime.date.today()
                next_seven_days = today + relativedelta(days=7)

                # create extended user data
                insert_ext_user = UserExtend(user=insert_user,
                                             is_suspended=0, 
                                             profile_pict_url=profile_pict, 
                                             sex=gender, 
                                             address=address,
                                             # phone_number=phone,
                                             # email_signature=email_signature, 
                                             create_date=now(),
                                             create_by=request.user.username, 
                                             is_activated=1,
                                             activation_key=activation_key,
                                             activation_expired_date=next_seven_days)
                insert_ext_user.save()

                # create default role
                role_group = RoleGroup.objects.get(pk=roles)
                insert_user_role = RoleUser(role_group=role_group, user=insert_user,
                                            create_date=now(), create_by=request.user.username)
                insert_user_role.save()


                transaction.savepoint_commit(sid)
            except IntegrityError as integrity_error:
                LOG.error(integrity_error)
                transaction.savepoint_rollback(sid)

            # Send Email Activation

            # host = settings.BACKEND_HOST_PROTOCOL + '://' + request.META['HTTP_HOST']
            # email_template = get_template('pln/email/activation_email.html')
            # email_template_param = {'activation_key': activation_key, 'current_host': host}
            # email_template_render = email_template.render(email_template_param)

            # send_mail_parameters = {
            #     'to': [email],
            #     'from': 'Perusahaan Listrik Negara <' + settings.DEFAULT_MAIL_FROM + '>',
            #     'subject': 'Aktivasi User Kamu -- Perusahaan Listrik Negara',
            #     'html': email_template_render
            # }

            # celery = Celery()
            # celery.config_from_object('django.conf:settings', namespace='CELERY')
            # try:
            #     celery.send_task("scheduler.tasks.send_mail_task", args=[send_mail_parameters], queue='celery',
            #                      routing_key='celery')
            # except Exception as exception:
            #     LOG.error(exception)

            response = redirect(reverse('user_list'))
            response.set_cookie('success_msg', 'Success Added New User', max_age=2)
            return response
        else:
            response = redirect(reverse('user_list'))
            response.set_cookie('error_msg', 'Error : ' + str(str(form.errors)), max_age=2)
            return response

    return render(request, 'backend/user-management/add-edit.html', data)


def detail(request, id=0):

    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        response = redirect(reverse('user_list'))
        response.set_cookie('error_msg', 'User Not Found', max_age=2)
        return response

    data = {
        'title': settings.GLOBAL_TITLE + ' | Profile - ' + user.first_name + ' ' + user.last_name,
        'sub_title': 'User Detail',
        'user': user,
        'active_menu': 'admin',
        'sub_menu': 'admin_user',
        'form': EditUserForm(),
        'roles': RoleGroup.objects.filter()
    }

    if request.method == 'POST':
        form = EditUserForm(request.POST)
        ext_user = user.admin_user
        user_role = user.roleuser

        if form.is_valid():

            cleaned_data = form.clean()

            first_name = str(cleaned_data.get('first_name')).lower()
            last_name = str(cleaned_data.get('last_name')).lower()
            gender = cleaned_data.get('gender')
            address = str(cleaned_data.get('address'))
            # phone = str(cleaned_data.get('phone')).lower()
            # email_signature = str(cleaned_data.get('email_signature')).lower()
            new_role = cleaned_data.get('roles')
            profile_pict = user.admin_user.profile_pict_url
            if 'images' in request.FILES:
                profile_pict = uploads('profile-pictures', request.FILES['images'])


            # start transaction
            sid = transaction.savepoint()

            try:
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                ext_user.sex = gender
                ext_user.address = address
                # ext_user.phone_number = phone
                # ext_user.email_signature = email_signature
                ext_user.profile_pict_url = profile_pict

                ext_user.save()

                if int(user_role.role_group_id) != int(new_role):
                    user_role.role_group_id = new_role
                    user_role.modify_date = now()
                    user_role.modified_by = request.user.username
                    user_role.save()

                transaction.savepoint_commit(sid)
            except IntegrityError as error:
                LOG.error(error)
                transaction.savepoint_rollback(sid)

            data['user'] = user

            response = redirect(reverse('user_detail', args=[id]))
            response.set_cookie('success_msg', 'Success Updated User', max_age=2)

            return response
        else:
            response = redirect(reverse('user_list'))
            response.set_cookie('error_msg', 'Error : ' + str(str(form.errors)), max_age=2)
            return response
    return render(request, 'backend/user-management/detail.html', data)


def delete(request, id=0):

    try:
        user_remove = User.objects.get(pk=id)
    except User.DoesNotExist:
        return redirect(reverse('user_list'))

    sid = transaction.savepoint()
    try:
        user_remove.is_active = False
        user_remove.save()

        pln_user = user_remove.pln_user
        pln_user.is_deleted = True
        pln_user.save()
    except IntegrityError as integrity_error:
        LOG.error(integrity_error)
        transaction.savepoint_rollback(sid)

        response = redirect(reverse('user_list'))
        response.set_cookie('error_msg', 'Failed Deleted User, Unknown Error', max_age=2)
        return response

    response = redirect(reverse('user_list'))
    response.set_cookie('success_msg', 'Success Deleted User', max_age=2)
    return response


def generate_act_key(key):
    keys = str(key)
    # last format actKey == hash('sha1','--'.time().'--'.$username.'--'),
    salt = str(hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5])
    act_key = hashlib.sha1(str(salt + keys).encode('utf-8')).hexdigest()
    return act_key


def user_activation(request):
    data = {'title': 'PLN | E-Request System - User Activation'}
    response = redirect(reverse('signin'))

    if 'act_key' not in request.GET:
        response.set_cookie('error_msg', 'Failed Activated User', max_age=2)
        return response

    activation_key = request.GET.get('act_key')
    try:
        user_ext = UserExtend.objects.get(activation_key=activation_key)
    except UserExtend.DoesNotExist:
        response.set_cookie('error_msg', 'Failed Activated User', max_age=2)
        return response

    today = datetime.datetime.now()
    if today.date() > user_ext.activation_expired_date:
        response.set_cookie('error_msg', 'Failed Activated User, Expired Activation Time', max_age=2)
        return response

    if user_ext.is_activated and user_ext.user.is_active:
        response.set_cookie('error_msg', 'User has been actived, please login', max_age=2)
        return response

    # start transaction
    sid = transaction.savepoint()

    try:
        user = User.objects.get(id=user_ext.user_id)

        default_password = password_generator()
        user.set_password(default_password)
        user.is_active = True
        user.save()

        user_ext.is_activated = True
        user_ext.save()

        transaction.savepoint_commit(sid)
    except IntegrityError as integrity_error:
        LOG.error(integrity_error)
        transaction.savepoint_rollback(sid)

        response.set_cookie('error_msg', 'Failed Activated User, Unknown Error', max_age=2)
        return response

    # Send Email Success Activation
    host = settings.BACKEND_HOST_PROTOCOL + '://' + request.META['HTTP_HOST']

    email_template = get_template('pln/email/success_activated_user.html')
    email_template_param = {'username': user.email, 'password': default_password,
                                    'host': host}
    email_template_render = email_template.render(email_template_param)

    send_mail_parameters = {
        'to': [user.email],
        'from': 'Perusahaan Listrik Negara <' + settings.DEFAULT_MAIL_FROM + '>',
        'subject': 'Anda Sukses Melakukan Aktivasi User',
        'html': email_template_render
    }

    try:
        celery = Celery()
        celery.config_from_object('django.conf:settings', namespace='CELERY')
        celery.send_task("scheduler.tasks.send_mail_task", args=[send_mail_parameters],
                         queue='celery', routing_key='celery')
    except Exception as exception:
        LOG.error(exception)

    return render(request, 'pln/backend/success_activated_user.html', data)


def manual_active_deactive_user(request, id=0):

    response = redirect(reverse('user_detail', args=[id]))

    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        response.set_cookie('error_msg', "User doesn't exists", max_age=2)
        return response

    if user.is_active == False:

        # if user.is_active and user.admin_user.is_activated:
        #     response.set_cookie('error_msg', 'User has been actived, please login', max_age=2)
        #     return response

        # start transaction
        sid = transaction.savepoint()
        try:
            user.is_active = True
            user.save()

            user_ext = user.admin_user
            user_ext.is_activated = 1
            user_ext.save()
        except IntegrityError as integrity_error:

            LOG.error(integrity_error)
            transaction.savepoint_rollback(sid)
            response.set_cookie('error_msg', 'Failed Activated User, Unknown Error', max_age=2)
            return response

        response = redirect(reverse('user_detail', args=[id]))
        response.set_cookie('success_msg', 'Success Activated User', max_age=2)
        return response
    else:

        # start transaction
        sid = transaction.savepoint()
        try:
            user.is_active = False
            user.save()

            user_ext = user.admin_user
            user_ext.is_activated = 0
            user_ext.save()
        except IntegrityError as integrity_error:

            LOG.error(integrity_error)
            transaction.savepoint_rollback(sid)
            response.set_cookie('error_msg', 'Failed Deactivated User, Unknown Error', max_age=2)
            return response

        response = redirect(reverse('user_detail', args=[id]))
        response.set_cookie('success_msg', 'Success Deactivated User', max_age=2)
        return response


def reset_password(request, id=0):

    response = redirect(reverse('user_detail', args=[id]))

    try:
        user = User.objects.get(pk=id)
        default_password = password_generator()
        user.set_password(default_password)
        user.save()
    except User.DoesNotExist:
        response.set_cookie('error_msg', "User doesn't exists", max_age=2)
        return response

    # Send Email Success Activation
    host = settings.BACKEND_HOST_PROTOCOL + '://' + request.META['HTTP_HOST']
    email_template = get_template('pln/email/success_reset_password_user.html')
    email_template_param = {'username': user.email, 'password': default_password,
                                    'host': host}
    email_template_render = email_template.render(email_template_param)

    send_mail_parameters = {
        'to': [user.email],
        'from': 'Perusahaan Listrik Negara <' + settings.DEFAULT_MAIL_FROM + '>',
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

    response.set_cookie('success_msg', "Success reset password user", max_age=2)
    return response