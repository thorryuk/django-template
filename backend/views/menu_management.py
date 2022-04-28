import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.timezone import now
from django_datatables_view.base_datatable_view import BaseDatatableView

from backend.forms import NewRoleForm
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

        return Menu.objects.filter().order_by('id', 'parent_menu_id')

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
                item.name,
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


def show_role_detail(request, id=0):

    try:
        role = RoleGroup.objects.get(pk=id)
    except RoleGroup.DoesNotExist:
        response = redirect(reverse('role_list'))
        response.set_cookie('error_msg', 'Role doesn\'t exits', max_age=2)
        return response
    
    data = {
        'title': settings.GLOBAL_TITLE + ' | Role Detail',
        'sub_title': 'Detail & Edit Role',
        'active_menu': 'admin',
        'sub_menu': 'admin_role',
        'menus': Menu.objects.filter().order_by('order'),
        'role': role
    }


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

    return render(request, 'backend/role-management/add-edit.html', data)


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

    data = {
        'title': settings.GLOBAL_TITLE + ' | Menu Add',
        'sub_title': 'Add New Menu',
        'active_menu': 'admin',
        'sub_menu': 'admin_menu',
        'form': NewRoleForm(),
        'menus': Menu.objects.filter().order_by('order')
    }

    if request.method == 'POST':
        data['form'] = NewRoleForm(request.POST)
        form = data['form']

        if form.is_valid():

            cleaned_data = form.clean()

            # start transaction
            sid = transaction.savepoint()
            try:

                new_role = RoleGroup(
                    name=cleaned_data.get('name').lower()
                    ,
                    description=cleaned_data.get('description'),
                    create_date=now(), 
                    create_by=request.user.username
                )
                new_role.save()
                transaction.savepoint_commit(sid)
            except IntegrityError as error:
                LOG.error(error)
                transaction.savepoint_rollback(sid)

                response = redirect(reverse('menu_list'))
                response.set_cookie('error_msg', 'Failed add role ' + str(error), max_age=2)
                return

            response = redirect(reverse('menu_list'))
            response.set_cookie('success_msg', 'Success add new role', max_age=2)
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
