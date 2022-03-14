from django.shortcuts import render


def page_not_found(request, reason=''):

    data = {'title': 'Error 404: Halaman Tidak Ditemukan',
            'message': 'Error 404: Halaman Tidak Ditemukan.'}
    return render(request, 'pln/error/404.html', data)