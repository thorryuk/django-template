import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse

from backend.forms import ProfileForm, ChangePasswordForm
from app.common_functions import handle_uploaded_file_local, password_check

LOG = logging.getLogger(__name__)


def show_profile_user(request):

    data = {'title': 'PPA | E-Reqruitment System - User Profile',
            'sub_title': 'Profile',
            'form': ProfileForm()}

    try:
        user = User.objects.get(email=request.user.email)
        data['user'] = user
    except User.DoesNotExist:
        return redirect(reversed('signout'))

    if request.method == 'POST':

        form = ProfileForm(request.POST)
        ext_user = user.nippon_user

        if form.is_valid():

            cleaned_data = form.clean()

            first_name = str(cleaned_data.get('first_name')).lower()
            last_name = str(cleaned_data.get('last_name')).lower()
            gender = cleaned_data.get('gender')
            address = str(cleaned_data.get('address'))
            phone = str(cleaned_data.get('phone')).lower()
            email_signature = str(cleaned_data.get('email_signature')).lower()

            profile_pict = ''
            if 'profile_pict' in request.FILES:
                local_path = settings.BASE_DIR + '/static/profile_pictures/'
                file_name = handle_uploaded_file_local(request.FILES['profile_pict'], local_path)
                profile_pict = settings.BACKEND_HOST_PROTOCOL + request.META['HTTP_HOST'] + \
                               settings.DEFAULT_PATH_PROFILE_PICT + file_name

            # start transaction
            sid = transaction.savepoint()

            try:
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                ext_user.sex = gender
                ext_user.address = address
                ext_user.phone_number = phone
                ext_user.email_signature = email_signature

                if profile_pict != '' :
                    ext_user.profile_pict_url = profile_pict

                ext_user.save()

                transaction.savepoint_commit(sid)
            except IntegrityError as error:
                LOG.error(error)
                transaction.savepoint_rollback(sid)

            data['user'] = user

            # response = render(request, 'pln/backend/admin_user_detail.html', data)
            response = redirect(reverse('profile'))
            response.set_cookie('success_msg', 'Success Edited User Profile', max_age=2)

            return response

    return render(request, 'pln/backend/profile.html', data)


def change_password(request):

    data = {'title': 'PPA | E-Reqruitment System - Change Password',
            'sub_title': 'Profile',
            'form': ChangePasswordForm()}

    if request.method == 'POST':

        response = redirect(reverse('change_password'))

        form = ChangePasswordForm(request.POST)

        if form.is_valid():

            cleaned_data = form.clean()

            old_password = str(cleaned_data.get('old_password'))
            new_password = str(cleaned_data.get('new_password'))
            confirm_new_password = str(cleaned_data.get('confirm_new_password'))

            if not request.user.check_password(old_password):
                response.set_cookie('error_msg', 'Failed change password, old password not match',
                                    max_age=2)
                return response

            if new_password != confirm_new_password:
                response.set_cookie('error_msg', 'Failed change password, new password not match '
                                                 'with confirm new password',
                                    max_age=2)
                return response

            if old_password == new_password:
                response.set_cookie('error_msg',
                                    'Failed change password, new password cannot same with old password',
                                    max_age=2)
                return response

            validate_password = password_check(new_password)
            if not validate_password['password_ok']:
                response.set_cookie('error_msg',
                                    'Failed change password, new password must contain min 8 char, '
                                    '1 symbol, 1 digit, 1 uppercase & 1 lowercase',
                                    max_age=2)
                return response

            try:
                user = User.objects.get(email=request.user.email)
                data['user'] = user
            except User.DoesNotExist:
                return redirect(reversed('signout'))

            user.set_password(new_password)
            user.save()

            response = redirect(reverse('signout'))
            response.set_cookie('success_msg', 'Success Change Password', max_age=2)
            return response

    return render(request, 'pln/backend/change_password.html', data)
