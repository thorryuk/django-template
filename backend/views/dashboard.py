from django.shortcuts import render


def show_dashboard(request):

    data = {'title': 'PPA | E-Reqruitment System - Dashboard',
            'sub_title': 'Dashboard',
            'email' : '',
            'name': '',
            'active_menu': 'dashboard'}

    return render(request, 'backend/dashboard.html', data)
