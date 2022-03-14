from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from frontend.views.authentication import do_login, do_logout, do_register, user_activation, forgot_password, reset_password, testing_data
from frontend.views.default_view import unknown_page, test_encrypt, index, about, gallery, profile, dashboard

from frontend.views.js_api import get_kotakabupaten_by_provinsi, get_kecamatan_by_kotakabupaten, get_kelurahan_by_kecamatan
from frontend.views.unit_management import show_list_unit, detail_unit, add_unit, GetUnitList
from frontend.views.permohonan_management import add_permohonan, GetPermohonanList, show_list_permohonan, detail_permohonan, detail_unit, download_excel, show_list_permohonan_unit, GetPermohonanUnitList

handler404 = 'ppa.views.default_view.page_not_found'
handler400 = 'ppa.views.default_view.page_not_found'
handler500 = 'ppa.views.default_view.page_not_found'

app_name = 'frontend'

urlpatterns = [

    # testing data

    url(r'^test/$', testing_data, name='test'),

    # JS API URL
    url(r'^api/kota-kabupaten', get_kotakabupaten_by_provinsi, name='get_kota_kabupaten'),
    url(r'^api/kecamatan', get_kecamatan_by_kotakabupaten, name='get_kecamatan'),
    url(r'^api/kelurahan', get_kelurahan_by_kecamatan, name='get_kelurahan'),

    # menu url
    url(r'^$', index, name='index'),
    url(r'^about/$', about, name='about'),
    url(r'^gallery/$', gallery, name='gallery'),
    url(r'^profile/$', login_required()(profile), name='profile'),
    url(r'^dashboard/$', login_required()(dashboard), name='dashboard'),

    # authentication
    url(r'^login/$', do_login, name='login'),
    url(r'^logout/$', do_logout, name='logout'),
    url(r'^register/$', do_register, name='register'),
    url(r'^activation/$', user_activation, name='user_activation'),
    url(r'^lupa-password/$', forgot_password, name='forgot_password'),
    url(r'^ubah-password/(?P<key>[\w\-]+)/$', reset_password, name='reset_password'),

    # unit management
    url(r'^unit/$', login_required()(show_list_unit), name='list_unit'),
    url(r'^unit/add/$', login_required()(add_unit), name='add_unit'),
    url(r'^unit/detail/(?P<id>[0-9]+)/$', login_required()(detail_unit), name='detail_unit'),
    url(r'^unit/ajax_list/$', GetUnitList.as_view(), name='unit_list_ajax'),

    # permohonan management
    url(r'^permohonan/add/$', login_required()(add_permohonan), name='add_permohonan'),
    url(r'^permohonan/$', login_required()(show_list_permohonan), name='list_permohonan'),
    url(r'^permohonan/ajax_list/$', GetPermohonanList.as_view(), name='permohonan_list_ajax'),
    url(r'^permohonan/detail/(?P<id>[0-9]+)/$', login_required()(detail_permohonan), name='detail_permohonan'),
    url(r'^permohonan/detail/unit/(?P<id>[0-9]+)/$', login_required()(detail_unit), name='detail_unit'),
    url(r'^permohonan/download/$', login_required()(download_excel), name='download_excel'),

    url(r'^permohonan/unit/(?P<id>[0-9]+)/$', login_required()(show_list_permohonan_unit), name='list_permohonan_unit'),
    url(r'^permohonan/unit/ajax_list/$', GetPermohonanUnitList.as_view(), name='permohonan_unit_list_ajax'),


]
