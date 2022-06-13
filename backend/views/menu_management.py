import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.timezone import now
from django_datatables_view.base_datatable_view import BaseDatatableView

from backend.forms import MenuForm
from backend.models import RoleGroup, RoleUser, Menu, RoleMenu

LOG = logging.getLogger(__name__)


def show_menu(request):
    data = {
        'title': settings.GLOBAL_TITLE + ' | Menu List',
        'sub_title': 'Menu Management',
        'active_menu': 'admin',
        'sub_menu': 'admin_menu'
    }

    return render(request, 'backend/menu-management/list.html', data)


class GetMenuList(BaseDatatableView):

    def get_initial_queryset(self):

        return Menu.objects.filter().order_by('-is_left_menu', '-parent_menu_id')

    def prepare_results(self, qs):

        json_data = []
        for index, item in enumerate(qs):

            # delete_link = ''
            # is_role_has_been_used = RoleUser.objects.filter(role_group_id=item.id)
            # if not is_role_has_been_used:
            #     delete_link = '<a class="btn btn-sm btn-alt-secondary" data-bs-toggle="tooltip" title="Delete" onclick="return confirm(\'Are you sure to delete this role?\'); " href="' + reverse('role_delete', args=[item.id]) + '">' + \
            #                   '<i class="fa fa-times"></i></a> '

            json_data.append([
                index + 1,
                item.id,
                '<a href="' + reverse('menu_detail', args=[item.id]) + '">' + item.name + '</a>',
                item.parent_menu_id,
                item.alias_name,
                item.is_left_menu,
                item.link,
                item.icon,
                item.is_tree,
                # '<div class="btn-group">' \
                # '<a class="btn btn-sm btn-alt-secondary" data-bs-toggle="tooltip" title="Edit" href="' + reverse('role_detail', args=[item.id]) + '">' \
                # '<i class="fa fa-pencil-alt"></i></a> ' + delete_link +
                # '</div>'
            ])

        return json_data


def detail_menu(request, id=0):

    try:
        menu = Menu.objects.get(pk=id)
    except Menu.DoesNotExist:
        response = redirect(reverse('menu_list'))
        response.set_cookie('error_msg', 'Menu doesn\'t exits', max_age=2)
        return response
    
    data = {
        'title': settings.GLOBAL_TITLE + ' | Menu Detail',
        'sub_title': 'Detail & Edit Menu',
        'active_menu': 'admin',
        'sub_menu': 'admin_menu',
        'menu': menu,
        'form': MenuForm(),
        'parent_menu': Menu.objects.filter(is_left_menu=True).order_by('order')
    }

    return render(request, 'backend/menu-management/add-edit.html', data)


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


def add_menu(request):

    menu = Menu.objects

    data = {
        'title': settings.GLOBAL_TITLE + ' | Menu Add',
        'sub_title': 'Add New Menu',
        'active_menu': 'admin',
        'sub_menu': 'admin_menu',
        'form': MenuForm(),
        'menus': menu.filter().order_by('order'),
        'parent_menu': menu.filter(is_left_menu=True).order_by('order')
    }

    if request.method == 'POST':
        data['form'] = MenuForm(request.POST)
        form = data['form']

        if form.is_valid():

            cleaned_data = form.clean()

            # start transaction
            sid = transaction.savepoint()
            try:
                new_menu = Menu(
                    name=cleaned_data.get('name'),
                    alias_name=cleaned_data.get('alias_name'),
                    parent_menu_id=cleaned_data.get('parent_menu'),
                    link=cleaned_data.get('link'),
                    icon=cleaned_data.get('icon'),
                    is_left_menu=cleaned_data.get('left_menu'),
                    is_tree=cleaned_data.get('tree')
                )
                new_menu.save()
                transaction.savepoint_commit(sid)
            except IntegrityError as error:
                LOG.error(error)
                transaction.savepoint_rollback(sid)

                response = redirect(reverse('menu_list'))
                response.set_cookie('error_msg', 'Failed add menu ' + str(error), max_age=2)
                return

            response = redirect(reverse('menu_list'))
            response.set_cookie('success_msg', 'Success add new menu', max_age=2)
            return response

        else:
            response = redirect(reverse('menu_list'))
            response.set_cookie('error_msg', 'Error : ' + str(str(form.errors)), max_age=2)
            return response
    return render(request, 'backend/menu-management/add-edit.html', data)


def show_role_user(request, id=0):

    try:
        role = RoleGroup.objects.get(pk=id)
    except RoleGroup.DoesNotExist:
        response = redirect(reverse('role_list'))
        response.set_cookie('error_msg', 'Role doesn\'t exits', max_age=2)
        return response

    data = {
        'title': settings.GLOBAL_TITLE + ' | Role User List',
        'sub_title': 'Role {}'.format(role.name.capitalize()),
        'active_menu': 'admin',
        'sub_menu': 'admin_role',
        'role_id': id
    }

    return render(request, 'backend/role-management/list-roleuser.html', data)


class GetRoleUserList(BaseDatatableView):

    def get_initial_queryset(self):

        return RoleUser.objects.filter(role_group_id=int(self.kwargs.get('id'))).order_by('-id')

    def prepare_results(self, qs):

        json_data = []
        for index, item in enumerate(qs):

            json_data.append([
                index + 1,
                # item.role_group.name,
                item.user.first_name + ' ' + item.user.last_name,
                '<a class="btn btn-info" href="' + reverse('user_detail', args=[item.user_id]) + '">'
                '<i class="fa fa-search"></i></a> '
            ])

        return json_data
