import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.timezone import now


from backend.forms import ChangePasswordForm, EditUserForm
from app.common_functions import password_check, uploads
from backend.models import RoleGroup


LOG = logging.getLogger(__name__)


def profile(request):

    id = request.user.id

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
        # 'active_menu': 'admin',
        # 'sub_menu': 'admin_user',
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

            response = redirect(reverse('profile'))
            response.set_cookie('success_msg', 'Success Updated User', max_age=2)

            return response
        else:
            response = redirect(reverse('user_list'))
            response.set_cookie('error_msg', 'Error : ' + str(str(form.errors)), max_age=2)
            return response
    return render(request, 'backend/user-management/profile.html', data)


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
