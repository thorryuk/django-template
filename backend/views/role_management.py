import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.timezone import now
from django_datatables_view.base_datatable_view import BaseDatatableView

from backend.forms import NewRoleForm
from backend.models import RoleGroup, RoleUser, Menu, RoleMenu

LOG = logging.getLogger(__name__)


def show_role(request):
    data = {'title': 'PPA | E-Reqruitment System - Role Management',
            'sub_title': 'Role Management',
            'active_menu': 'admin_role'}

    return render(request, 'pln/backend/admin_role_list.html', data)


class GetRoleList(BaseDatatableView):

    def get_initial_queryset(self):

        return RoleGroup.objects.filter().order_by('-id')

    def prepare_results(self, qs):

        json_data = []
        for index, item in enumerate(qs):

            delete_link = ''
            is_role_has_been_used = RoleUser.objects.filter(role_group_id=item.id)
            if not is_role_has_been_used:
                delete_link = ' | <a class="btn btn-red" onclick="return confirm(\'Are you sure to delete this role?\'); " href="' + reverse('role_delete', args=[item.id]) + '">' + \
                              '<i class="fa fa-trash"></i></a> '

            json_data.append([
                index + 1,
                '<a href="' + reverse('role_user', args=[item.id]) + '">' + item.name + '</a>',
                item.description,
                '<a class="btn btn-info" href="' + reverse('role_detail', args=[item.id]) + '">'
                '<i class="fa fa-search"></i></a> ' + delete_link
            ])

        return json_data


def show_role_detail(request, id=0):

    data = {'title': 'PPA | E-Reqruitment System - Role Management',
            'sub_title': 'Role Management - Detail',
            'active_menu': 'admin_role',
            'menus': Menu.objects.filter().order_by('order')}

    try:
        role = RoleGroup.objects.get(pk=id)
    except RoleGroup.DoesNotExist:
        response = redirect(reverse('role_list'))
        response.set_cookie('error_msg', 'Role doesn\'t exits', max_age=2)
        return response

    data['role'] = role

    old_menu_selected_dict = {}
    for menu in role.rolemenu_set.all():
        old_menu_selected_dict[menu.menu_id] = menu.menu.name

    data['old_menu_selected_dict'] = old_menu_selected_dict

    if request.method == 'POST':
        menu_selected_list = request.POST.getlist('menus_selected[]')
        if menu_selected_list:

            # Delete old role
            role.rolemenu_set.all().delete()

            for menu_id in menu_selected_list:
                try:
                    new_role_menu = RoleMenu(menu_id=menu_id, role_group_id=id)
                    new_role_menu.save()
                except IntegrityError as error:
                    pass

        response = redirect(reverse('role_detail', args=[id]))
        response.set_cookie('success_msg', 'Success update role', max_age=2)
        return response

    return render(request, 'pln/backend/admin_role_detail.html', data)


def delete_role(request, id=0):

    try:
        role = RoleGroup.objects.get(pk=id)
    except RoleGroup.DoesNotExist:
        response = redirect(reverse('role_list'))
        response.set_cookie('error_msg', 'Role doesn\'t exists', max_age=2)
        return response

    # start transaction
    sid = transaction.savepoint()
    try:

        role.delete()
        transaction.savepoint_commit(sid)
    except IntegrityError as error:
        LOG.error(error)
        transaction.savepoint_rollback(sid)

        response = redirect(reverse('role_list'))
        response.set_cookie('error_msg', 'Failed delete role ' + str(error), max_age=2)
        return response

    response = redirect(reverse('role_list'))
    response.set_cookie('success_msg', 'Success delete role', max_age=2)
    return response


def add_role(request):

    data = {'title': 'PPA | E-Reqruitment System - Role Management',
            'sub_title': 'Role Management - Add',
            'active_menu': 'admin_role',
            'form': NewRoleForm()}

    if request.method == 'POST':
        data['form'] = NewRoleForm(request.POST)
        form = data['form']

        if form.is_valid():

            cleaned_data = form.clean()

            # start transaction
            sid = transaction.savepoint()
            try:

                new_role = RoleGroup(name=cleaned_data.get('name'),
                                     description=cleaned_data.get('description'),
                                     create_date=now(), create_by=request.user.username)
                new_role.save()
                transaction.savepoint_commit(sid)
            except IntegrityError as error:
                LOG.error(error)
                transaction.savepoint_rollback(sid)

                response = redirect(reverse('role_list'))
                response.set_cookie('error_msg', 'Failed add role ' + str(error), max_age=2)
                return response

            response = redirect(reverse('role_list'))
            response.set_cookie('success_msg', 'Success add new role', max_age=2)
            return response

    return render(request, 'pln/backend/admin_add_role.html', data)


def show_role_user(request, id=0):
    data = {'title': 'PPA | E-Reqruitment System - Role Management',
            'active_menu': 'admin_role',
            'role_id': id}

    try:
        role = RoleGroup.objects.get(pk=id)
    except RoleGroup.DoesNotExist:
        response = redirect(reverse('role_list'))
        response.set_cookie('error_msg', 'Role doesn\'t exits', max_age=2)
        return response

    data['sub_title'] = 'Role {} User List'.format(role.name.capitalize())

    return render(request, 'pln/backend/admin_role_user_list.html', data)


class GetRoleUserList(BaseDatatableView):

    def get_initial_queryset(self):

        return RoleUser.objects.filter(role_group_id=int(self.kwargs.get('id'))).order_by('-id')

    def prepare_results(self, qs):

        json_data = []
        for index, item in enumerate(qs):

            json_data.append([
                index + 1,
                item.role_group.name,
                item.user.first_name + ' ' + item.user.last_name,
                '<a class="btn btn-info" href="' + reverse('user_detail', args=[item.user_id]) + '">'
                '<i class="fa fa-search"></i></a> '
            ])

        return json_data
