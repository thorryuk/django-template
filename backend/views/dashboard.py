from django.shortcuts import render
from django.conf import settings


def show_dashboard(request):

    data = {'title': settings.GLOBAL_TITLE + ' | Dashboard',
            'sub_title': 'Dashboard',
            'email' : '',
            'name': '',
            'active_menu': 'dashboard'}

    return render(request, 'backend/dashboard.html', data)
