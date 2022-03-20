"""putra perkasa abadi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from backend.views.dashboard import show_dashboard
from backend.views.forget_password import show_forget_password, do_reset_password
from backend.views.js_api import get_city_by_country, get_user_by_role
from backend.views.login import do_login, do_logout
from backend.views.role_management import show_role, GetRoleList, show_role_detail, delete_role, add_role, show_role_user, GetRoleUserList
from backend.views.user_management import show_user_list, add_new_user, detail, delete, \
    user_activation, manual_active_deactive_user, reset_password
from backend.views.user_profile import show_profile_user, change_password
from app.common_functions import validate_user_entry_menu


handler404 = 'app.views.custom_default_view.page_not_found'
handler400 = 'app.views.custom_default_view.page_not_found'
handler500 = 'app.views.custom_default_view.page_not_found'

app_name = 'cms'

urlpatterns = [

    # Main URL
    url(r'^$', do_login, name='signin_default'),
    url(r'^signin/$', do_login, name='signin'),
    url(r'^signout/$', do_logout, name='signout'),
    url(r'^forget_password/$', show_forget_password, name='forget_password'),
    url(r'^reset_password/$', do_reset_password, name='do_reset_password'),
    url(r'^activation/$', user_activation, name='user_activation'),

    
    # Dashboard URL
    url(r'^dashboard/$', login_required()(validate_user_entry_menu(1)(show_dashboard)),
        name='dashboard'),
    # url(r'^dashboard/$', show_dashboard, name='dashboard'),

    
    # User Profile
    url(r'^profile/$', login_required(show_profile_user),name='profile'),
    url(r'^change-password/$', login_required(change_password),name='change_password'),


    # JS API
    url(r'^api/city_by_country', get_city_by_country, name='get_city_by_country'),
    url(r'^api/user_by_role', get_user_by_role, name='get_user_by_role'),


    # Administrator User URL
    url(r'^administrator/user/$', login_required()(validate_user_entry_menu(18)(show_user_list)),
        name='user_list'),
    url(r'^administrator/user/add/$', login_required()(validate_user_entry_menu(19)(add_new_user)),
        name='add_user'),
    url(r'^administrator/user/detail/(?P<id>[0-9]+)/$',
        login_required()(validate_user_entry_menu(20)(detail)), name='user_detail'),
    url(r'^administrator/user/delete/(?P<id>[0-9]+)/$',
        login_required()(validate_user_entry_menu(57)(delete)), name='user_delete'),
    url(r'^administrator/user/manual-activation/(?P<id>[0-9]+)/(?P<types>[a-z]+)/$',
        login_required()(validate_user_entry_menu(101)(manual_active_deactive_user)),
        name='user_manual_activation'),
    url(r'^administrator/user/reset-password/(?P<id>[0-9]+)/$',
        login_required()(validate_user_entry_menu(102)(reset_password)), name='user_reset_password'),


    # Role Management
    url(r'^administrator/role/list/$', login_required()(validate_user_entry_menu(47)(show_role)),
        name='role_list'),
    url(r'^administrator/role/user/(?P<id>[0-9]+)/$',
        login_required()(validate_user_entry_menu(98)(show_role_user)), name='role_user'),
    url(r'^administrator/role/user/ajax/(?P<id>[0-9]+)/$', GetRoleUserList.as_view(),
        name='role_user_ajax'),
    url(r'^administrator/role/list/ajax/$', GetRoleList.as_view(), name='role_list_ajax'),
    url(r'^administrator/role/detail/(?P<id>[0-9]+)/$',
        login_required()(validate_user_entry_menu(49)(show_role_detail)), name='role_detail'),
    url(r'^administrator/role/delete/(?P<id>[0-9]+)/$',
        login_required()(validate_user_entry_menu(97)(delete_role)), name='role_delete'),
    url(r'^administrator/role/add/$', login_required()(validate_user_entry_menu(48)(add_role)),
        name='add_role'),

]
