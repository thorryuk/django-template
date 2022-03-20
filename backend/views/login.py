from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout_then_login
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.conf import settings


from backend.forms import LoginForm
from backend.models import RoleUser


def do_login(request):

    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))

    form = LoginForm()
    data = {
        'form': form, 
        'title': settings.GLOBAL_TITLE + ' | Login'
    }

    if request.POST:

        response = redirect(reverse('signin'))
        form = LoginForm(request.POST)
        form_valid = form.is_valid()

        if form_valid:

            cleaned_data = form.cleaned_data
            email = cleaned_data['email']
            password = cleaned_data['password']
            email = email.lower()

            try:
                user = authenticate(username=email, password=password, is_staff=True)
            except MultipleObjectsReturned:
                pass

            if user is None:
                response.set_cookie('error_msg', 'Login failed!', max_age=2)
                return response

            if not user.is_active or not user.admin_user.is_activated:
                response.set_cookie('error_msg', 'Please activate your account', max_age=2)
                return response

            if user.admin_user.is_deleted is True:
                response.set_cookie('error_msg', 'Login failed!', max_age=2)
                return response

            user_left_menus = []
            user_menu_id = []
            # Load Left Menu
            role_user = RoleUser.objects.get(user=user)
            for role_menu in role_user.role_group.rolemenu_set.all().order_by('menu__order'):
                if role_menu.menu.is_left_menu:
                    menu = {"menu_id": role_menu.menu.id,
                            "name": role_menu.menu.name,
                            'link': role_menu.menu.link,
                            'alias': role_menu.menu.alias_name,
                            'is_left': role_menu.menu.is_left_menu,
                            'parent_id': role_menu.menu.parent_menu_id,
                            'icon': role_menu.menu.icon,
                            'is_tree': role_menu.menu.is_tree}
                    user_left_menus.append(menu)
                user_menu_id.append(role_menu.menu_id)

            request.session['left_menu'] = user_left_menus
            request.session['menu'] = user_menu_id
            login(request, user)
            return redirect('dashboard')
        else:
            response.set_cookie('error_msg', 'Login failed!', max_age=2)
            return response

    return render(request, 'backend/login.html', data)


def do_logout(request):
    response = logout_then_login(request, reverse('signin'))
    return response